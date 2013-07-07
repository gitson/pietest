import unittest
import sys
sys.path.append('..')
import mainproc

class TestMainProcMethods(unittest.TestCase):

    def setUp(self):
    	mainproc.OUT = ''
    	mainproc.OUTPUT = mainproc.string_output

    def test_TEST_END(self):
    	# TEST followed by END
    	program="""// TEST: test1
// END
"""
    	mainproc.runner(program.splitlines(True))
    	self.assertEqual(mainproc.OUT, 
"""fprintf(stderr, "- test:\\n    name: test1\\n    content: \\n");
fprintf(stderr, "- ignore:\\n\\n");
""")

if __name__ == '__main__':
    unittest.main()