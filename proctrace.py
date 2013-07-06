import yaml, sys

ANY_ARG = 'ANY_ARG'
ANY_RET = 'ANY_RET'

TSP = ' '*4
ESP = ' '*8

class Check:
	def __init__(self, check):
		self.__dict__ = check
	def __str__(self):
		return str(self.line) + ': ' + self.expression + ': ' + str(self.value)
	def condition(self):
		return str(self.line) + ': ' + self.expression

class Call:
	@staticmethod
	def matchArgs(a, b):
		if a == b:
			return True
		else:
			if(len(a) == len(b)):
				for i in range(len(a)):
					if a[i] != b[i] and b[i] != ANY_ARG:
						return False
				return True
		return False

	@staticmethod
	def matchRet(a, b):
		return a == b or b == ANY_RET

	def __init__(self, call):
		self.__dict__ = call
		if not 'ret' in call.keys():
			self.ret = None
		if not 'args' in call.keys():
			self.args = []
			
	def __str__(self):
		return str(self.func) + '(' + ', '.join([str(arg) for arg in self.args]) + ')' + str(self.ret)


	def match(self, call):
		if self.func == '<STAR>':
			return True
		return self.func == call.func and Call.matchArgs(call.args, self.args) and Call.matchRet(call.ret, self.ret)

class Ret:
	def __init__(self, ret):
		self.__dict__ = ret

class TElement:
	def __init__(self, element, **attrs):
		self.attrs = attrs
		self.element = element

	def __str__(self):
		attrs = ' '.join([attr + '="' + value + '"' for attr, value in self.attrs.iteritems()])
		return '<' + self.element + ' ' + attrs + '>'

	def close(self):
		return '</' + self.element + '>'

class Test:
	def __init__(self, test):
		self.__dict__ = test
		telem = TElement('test', name=self.name)
		print(telem)
		self.gatherElements()
		self.showChecks()
		self.matchCallsRets()
		self.checkCalls()
		print(telem.close())

	def showChecks(self):
		for check in self.tchecks:
			if check.value == 0:
				print('  ' + str(TElement('check', line=str(check.line), expression=check.expression.replace('<NOT>', '!'))))

	def checkCalls(self):
		i = j = 0
		while i < len(self.tcalls) and j < len(self.calls):
			tcall = self.tcalls[i]
			call = self.calls[j]
			if tcall.func == '<STAR>':
				if i == len(self.tcalls) - 1:
					return
				else:
					i += 1
					tcall = self.tcalls[i]						
					while not tcall.match(call) and j < len(self.calls) - 1 and tcall.func != call.func:
						j += 1
						call = self.calls[j]
			if not tcall.match(call):
				print('  ' + str(TElement('call', expected=str(tcall), obtained=str(call))))
				return
			j += 1
			i += 1
		if i >= len(self.tcalls):
			if j < len(self.calls):
				print('  ' + str(TElement('call', expected='None', obtained=str(self.calls[j]))))
		else:
			if j >= len(self.calls):
				if i != len(self.tcalls) - 1 or self.tcalls[i].func != '<STAR>':
					print('  ' + str(TElement('call', expected=str(self.tcalls[i]), obtained='None')))

	def gatherElements(self):
		self.tchecks = []
		self.tcalls = []
		self.callsRets = []
		for item in self.content:
			if isinstance(item, dict):
				key = item.keys()[0]
				if key == 'tcheck':
					self.tchecks += [Check(item[key])]
				elif key == 'tcall':
					self.tcalls += [Call(item[key])]
				elif key == 'call':
					self.callsRets += [Call(item[key])]
				elif key == 'ret':
					self.callsRets += [Ret(item[key])]

	def matchCallsRets(self):
		xcalls = []
		self.calls = []
		for item in self.callsRets:
			if isinstance(item, Call):
				xcalls.append(item)
			else:
				call = xcalls.pop()
				if call.func == item.func:
					if item.val == 'None':
						item.val = None
					call.ret = item.val

		self.calls = [item for item in self.callsRets if isinstance(item, Call)]

	def __str__(self):
		return 'Test: ' + self.name + '\n' + str(self.content)

def proctrace(tests):
	for item in tests:
		if item.keys()[0] == 'test':
			test = Test(item['test'])

if __name__ == '__main__':
	filename = 'test.yaml'
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	with open(filename) as f:
		proctrace(yaml.load(f))