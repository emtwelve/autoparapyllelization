import ast

from sys import argv
if len(argv) != 2:
    print "Need program to analyze as argument"
    assert(False)

program = open(argv[1], 'r').read()

print "####\n", program, "####"

def cprint(node, s):
  """ Print s indented by node.col_offset """
  print " "*node.col_offset + s

class ArrayVisitor(ast.NodeVisitor):
  """ Visit array assignments / uses to gather
      information to use in array dependence
      analysis within a For loop """
  def visit_Assign(self, node):
    cprint(node, "Assign found")

class FuncVisitor(ast.NodeVisitor):
  """ Visit a function and find its loops """
  def visit_FunctionDef(self, node):
    cprint(node, "Function" + node.name)
    self.generic_visit(node) # visit children

  def visit_For(self, node):
    cprint(node, "For found")
    arrVisitor = ArrayVisitor()
    arrVisitor.visit(node)
  """
  def visit_Assign(self, node):
    print "Assign found"
  def visit_Return(self, node):
    print "Return found"
  """


tree = ast.parse(program)

print "####\n", ast.dump(tree), "####\n"

visitor = FuncVisitor()
visitor.visit(tree.body[0])