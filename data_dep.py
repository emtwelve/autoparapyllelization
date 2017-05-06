import ast
from copy import deepcopy

from sys import argv
if len(argv) != 2:
    print "Need program to analyze as argument"
    assert(False)

program = open(argv[1], 'r').read()

print "####\n", program, "####"

def cprint(node, s):
  """ Print s indented by node.col_offset """
  print " "*node.col_offset + s

LHS = None
RHS = None

class ReplaceWithConstant(ast.NodeTransformer):
  """ Replace variable with identifier id with a constant """
  def __init__(self, constant, _id):
    self.constant = constant; self.id = _id
  def visit_Name(self, node):
    self.generic_visit(node) # visit children
    if isinstance(node, ast.Name) and node.id == self.id:
      return ast.Num(self.constant)
    else:
      return node # don't change


def build_expression_map(v, LHS, RHS):
  exp_map = []

  for i in xrange(v.lower, v.upper, v.step):
    _LHS = deepcopy(LHS)
    _RHS = deepcopy(RHS)
    ReplaceWithConstant(i, v.id).visit(_LHS)
    ReplaceWithConstant(i, v.id).visit(_RHS)
    ast.fix_missing_locations(_LHS)
    ast.fix_missing_locations(_RHS)

    LHS_val = eval(compile(ast.Expression(_LHS), filename="<ast>", mode="eval"))
    RHS_val = eval(compile(ast.Expression(_RHS), filename="<ast>", mode="eval"))

    exp_map += [(_LHS, LHS_val, _RHS, RHS_val)]

  return exp_map

def computeExpression(exp_map, i, typ):
  if   typ == "LHS": return exp_map[i][1]
  elif typ == "RHS": return exp_map[i][3]
  else: print('invalid type'); assert(False)

class ArrayVisitor(ast.NodeVisitor):
  """ Visit array assignments / uses to gather
      information to use in array dependence
      analysis within a For loop """
  def __init__(self, _loopVar):
    self.arrays = []
    self.loopVar = _loopVar
  
  def visit_Assign(self, node):
    global LHS, RHS, hi
    cprint(node, "Assign found")
    LHS = node.targets[0].slice.value
    RHS = node.value.slice.value
    print str(self.loopVar)
    assert(len(node.targets) == 1)
    v = self.loopVar

    # Generate a mapping of
    #   Constant -> Expression computed with Value replaced with Constant
    exp_map = build_expression_map(v, LHS, RHS)

    has_independent_iterations = True
    print v.lower, v.upper, v.step
    for i in xrange(v.lower, v.upper, v.step):
      LHS_val = computeExpression(exp_map, i, "LHS")
      for j in xrange(v.lower, v.upper, v.step):
        RHS_val = computeExpression(exp_map, j, "RHS")

        print LHS_val, RHS_val

        if LHS_val == RHS_val:
          has_independent_iterations = False; break
      # break out of nested loop
      if has_independent_iterations == False: break
          

    print has_independent_iterations, LHS_val, RHS_val


class Iterator(object):
  def __init__(self, _id, lower, upper, step=1):
    self.id    = _id;     self.step  = step
    self.lower = lower.n; self.upper = upper.n
  def __str__(self):
    return self.id + ":" + "[" +   \
           str(self.lower) + "," + \
           str(self.upper) + "," + \
           str(self.step) + "]"

class FuncVisitor(ast.NodeVisitor):
  """ Visit a function and find its loops """
  def visit_FunctionDef(self, node):
    cprint(node, "Function" + node.name)
    self.generic_visit(node) # visit children

  def visit_For(self, node):
    cprint(node, "For found")

    loop_var_id = node.target.id
    fn_name = node.iter.func.id
    fn_args = node.iter.args
    assert(len(fn_args) in [1,2]) # TODO: add 3 for step argument
    assert(fn_name == "xrange" or fn_name == "range")

    loopVar = Iterator(loop_var_id, fn_args[0], fn_args[1])
    arrVisitor = ArrayVisitor(loopVar)
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