import os, sys, re

SEP = '\:'
TESTSex = re.compile('^\/\/\s*TEST\s*' + SEP + '\s*(\w+)\s*$')
TESTEex = re.compile('^\/\/\s*END\s*$')
CALLS = re.compile('^\/\/\s*CALLS\s*' + SEP + '(.*)$')
CHECK = re.compile('^\/\/\s*CHECK\s*' + SEP + '(.*)$')
EXP_NOT = '<NOT>'
MAIN_FILE = 'main.c'
STREAM = 'stderr'
MSP = 4 * ' '
TSP = 6 * ' '
ESP = 10 * ' '
OUT = ''

def print_output(s):
	print s
def string_output(s):
	global OUT
	OUT += str(s) + '\n'

OUTPUT = string_output

# --- internals ---

FNCALL = re.compile('^(.*)\(\s*(.*)\s*\)\s*(.*)$')

class TOutput:
	stream = 'stderr'
	def __init__(self, fmt, *pargs):
		self.internal_text = 'fprintf(' + TOutput.stream + ', \"' + fmt + '\\n\"' +\
							 (pargs and (', ' + ', '.join(pargs))  or '') + ');'
	def __repr__(self):
		return self.internal_text

class TCall(TOutput):
	@staticmethod
	def fmtCall(fnname, fnargs = None):
		args = ''
		if fnargs:
			args = ESP + 'args: [' + ', '.join(arg == '_' and 'ANY_ARG' or '0x%x' for arg in fnargs) + ']'
		return TSP + '- tcall:\\n' + ESP + 'func: ' + fnname + '\\n' + args

	@staticmethod
	def fmtRet(val):
		if val != '_':
			return val and '\\n' + ESP + 'ret: 0x%x' or ''
		else:
			return '\\n' + ESP + 'ret: ANY_RET'

	def __init__(self, call):
		if call == '*':
			call = '<STAR>'
			TOutput.__init__(self, TCall.fmtCall(call))
		else:
			rematch = re.match(FNCALL, call)
			if rematch:
				fnname = rematch.group(1).strip()
				args = rematch.group(2)
				val = rematch.group(3).strip()
				if val != '_':
					valout = val
				else:
					valout = []

				sargs = args.split(',')
				fnargs = [arg.strip() for arg in sargs]
				fnoutargs = [arg for arg in fnargs if arg != '_']
				TOutput.__init__(self, TCall.fmtCall(fnname, fnargs) + TCall.fmtRet(val),\
										  ', '.join(fnoutargs + (valout and [valout] or [])))

class TCheck(TOutput):
	@staticmethod
	def changeNot(expression):
		return expression.replace('!', EXP_NOT)

	def __init__(self, check, line_no):
		TOutput.__init__(self, TSP + '- tcheck:\\n' + ESP + 'expression: ' + TCheck.changeNot(check) + '\\n' + ESP +\
								'line: %d' + '\\n' + ESP + 'value: 0x%x', str(line_no), check)

def process_calls(calls):
	for call in calls:
		OUTPUT(TCall(call))

def process_checks(checks, line_no):
	for check in checks:
		OUTPUT(TCheck(check, line_no))

def runner(source):
		test_name = None
		line_no = 0
		for line in source:
			line_no += 1
			sline = line.lstrip()
			sline = sline.rstrip()
			rematch = re.match(TESTSex, sline)
			if rematch:
				test_name = rematch.group(1)
				OUTPUT(TOutput('- test:\\n' + MSP + 'name: ' + test_name + '\\n' + MSP + 'content: '))
				continue
			rematch = re.match(TESTEex, sline)
			if rematch:
				if test_name:
					test_name = None
					OUTPUT(TOutput('- ignore:\\n'))
				else:
					OUTPUT('Line ' + line_no + ': !!! ERROR: END without active TEST !!!\n')
				continue		
			if test_name:
				rematch = re.match(CALLS, sline)
				if rematch:
					calls = rematch.group(1).split(';')
					process_calls([call.strip() for call in  calls])
					continue
				rematch = re.match(CHECK, sline)
				if rematch:
					checks = rematch.group(1).split(';')
					process_checks([check.strip() for check in checks], line_no)
					continue		
			OUTPUT(line)

if __name__ == "__main__":
	with open(MAIN_FILE,'rt') as f:
		runner(f)
	if len(OUT) != 0:
		print OUT