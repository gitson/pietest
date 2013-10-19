#------------------------------------------------------------------------------
# Portions based on pycparser: c-to-c.py, (C) 2008-2012, Eli Bendersky, BSD license
#------------------------------------------------------------------------------
from __future__ import print_function
import sys
from mainproc import *

TEMP_VAR_NAME = 'e5b9b38b'
# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

from pycparser import parse_file, c_parser, c_generator, c_ast

class FuncArgsGenerator(c_generator.CGenerator):
    
    def _init_(self):
        self.reset_args()

    def reset_args(self):
        self.arg_types = self.arg_names = ()
        
    def visit_IdentifierType(self, n):
        self.arg_types += (n.names[0],)
        return ' '.join(n.names)
    
    def fmt_string(self):
        return ', '.join('0x%x' for x in self.arg_names[1:])

    def fmt_names(self):
        return ', '.join(self.arg_names[1:])

    def fmt_args(self):
        return str(TOutput('          args: [' + self.fmt_string() + ']', self.fmt_names())) + '\n'

    def _generate_type(self, n, modifiers=[]):
        typ = type(n)

        if typ == c_ast.TypeDecl:
            s = ''
            if n.quals: s += ' '.join(n.quals) + ' '
            s += self.visit(n.type)

            nstr = n.declname if n.declname else ''
            if n.declname: self.arg_names += (n.declname,)

            for i, modifier in enumerate(modifiers):
                if isinstance(modifier, c_ast.ArrayDecl):
                    if (i != 0 and isinstance(modifiers[i - 1], c_ast.PtrDecl)):
                        nstr = '(' + nstr + ')'
                    nstr += '[' + self.visit(modifier.dim) + ']'
                elif isinstance(modifier, c_ast.FuncDecl):
                    if (i != 0 and isinstance(modifiers[i - 1], c_ast.PtrDecl)):
                        nstr = '(' + nstr + ')'
                    nstr += '(' + self.visit(modifier.args) + ')'
                elif isinstance(modifier, c_ast.PtrDecl):
                    if modifier.quals:
                        nstr = '* %s %s' % (' '.join(modifier.quals), nstr)
                    else:
                        nstr = '*' + nstr
            if nstr: s += ' ' + nstr
            return s

        elif typ == c_ast.Decl:
            return self._generate_decl(n.type)
        elif typ == c_ast.Typename:
            return self._generate_type(n.type)
        elif typ == c_ast.IdentifierType:
            return ' '.join(n.names) + ' '
        elif typ in (c_ast.ArrayDecl, c_ast.PtrDecl, c_ast.FuncDecl):
            return self._generate_type(n.type, modifiers + [n])
        else:
            return self.visit(n)

class FuncCallsTracer(c_generator.CGenerator):
    
    cfunc = None
    func_args_gen = None

    def __init__(self):
        self.func_args_gen = FuncArgsGenerator()

    def fmt_Args(self, n):
        self.func_args_gen.reset_args()
        self.func_args_gen._generate_type(n.decl.type)
        return self.func_args_gen.fmt_args()
    
    def fmt_Return(self, n, stmt):
        if stmt and stmt.expr:
            expr = self.visit(stmt.expr)
            start_block = self._make_indent() + '{\n'
            self.indent_level += 2
            return_block = self._make_indent() +\
                                         'const ' + self.func_args_gen.arg_types[0] +\
                                         ' ' + TEMP_VAR_NAME + ' = ' + expr + ';\n' +\
                                         self._make_indent() +\
                                         str(TOutput('      - ret:\\n          func: %s\\n          val: 0x%x', '"' + self.cfunc.decl.name + '"', TEMP_VAR_NAME)) +\
                                         '\n' + self._make_indent() +\
                                         'return ' + TEMP_VAR_NAME + ';\n'

            self.indent_level -= 2
            end_block = self._make_indent() + '}\n'
            return start_block + return_block + end_block
        else:
            return self._make_indent() +\
                         str(TOutput('      - ret:\\n          func: %s\\n          val: None', '"' + self.cfunc.decl.name + '"')) +\
                         '\n' + self._make_indent() + 'return;\n'
                        
    def fmt_Call(self, n):
        return self._make_indent() +\
                     str(TOutput('      - call:\\n          func: %s', '"' + n.decl.name + '"')) +\
                     '\n' + self._make_indent() + self.fmt_Args(n)

    def visit_Compound(self, n):
        s = self._make_indent() + '{\n'
        self.indent_level += 2
        if n.block_items:
            for stmt in n.block_items:
                if isinstance(stmt, c_ast.Return):
                    if self.cfunc:
                        s += self.fmt_Return(self.cfunc, stmt)
                else:
                    s += self._generate_stmt(stmt)
        self.indent_level -= 2
        s += self._make_indent() + '}\n'
        return s

    def visit_FuncDef(self, n):
        self.cfunc = n
        decl = self.visit(n.decl)
        self.indent_level = 2
        body = '{\n' + self.fmt_Call(n) +\
                     self.visit(n.body)
        if self.func_args_gen.arg_types[0] == 'void': body += self.fmt_Return(n, None)
        body += '}'
                        
        if n.param_decls:
            knrdecls = ';\n'.join(self.visit(p) for p in n.param_decls)
            return '\n' + decl + '\n' + knrdecls + ';\n' + body + '\n'
        else:
            return '\n' + decl + '\n' + body + '\n'

def translate_to_c(filename):
    ast = parse_file(filename, use_cpp=True)
    generator = FuncCallsTracer()
    print('#include <stdio.h>\n' + generator.visit(ast))

#------------------------------------------------------------------------------

if __name__ == "__main__":
    filename = 'a.c'
    if len(sys.argv) > 1:
        filename = sys.argv[1] 
    translate_to_c(filename)
