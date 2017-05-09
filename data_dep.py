import ast
from copy import deepcopy
from sys import exit

from sys import argv
if len(argv) != 2:
    print "Need program to analyze as argument"
    assert(False)

program = open(argv[1], 'r').read()

print "####\n", program, "####"

def cprint(node, s):
  """ Print s indented by node.col_offset """
  print " "*node.col_offset + s

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

def opToStr(op):
  if isinstance(op, ast.Add): return "+"
  if isinstance(op, ast.Sub): return "-"
def buildExpressionString(E):
  bes = buildExpressionString
  if isinstance(E, ast.BinOp):
    return bes(E.left) + opToStr(E.op) + bes(E.right)
  if isinstance(E, ast.Name):
    return E.id
  if isinstance(E, ast.Num):
    return str(E.n)
def printExpression(E):
  print buildExpressionString(E)
def buildSubscriptString(S):
  arrayName = S.value.id
  index = S.slice.value
  return arrayName + "[" + buildExpressionString(index) + "]"
def printSubscript(S):
  assert(isinstance(S, ast.Subscript))
  print buildSubscriptString(S)

class ArrayAccess(object):
  def __init__(self, _array_name, _indexing_exp, _access_type, _iterators):
    self.array_name = _array_name
    self.access_type = _access_type
    self.indexing_exp = _indexing_exp
    self.iterators = _iterators
  def __str__(self):
    return "ACCESS{" + self.array_name + "[" + buildExpressionString(self.indexing_exp) + "]" + \
           " " + self.access_type + " " + str(self.iterators) + "}"
  def __repr__(self): return self.__str__()

class Iterator(object):
  def __init__(self, _id, lower, upper,  _depth, step=1):
    self.id    = _id;     self.step  = step
    self.lower = lower.n; self.upper = upper.n
    self.depth = _depth
  def __str__(self):
    return "ITER{" + str(self.depth) + ", " + \
           self.id + ":" + "[" +   \
           str(self.lower) + "," + \
           str(self.upper) + "," + \
           str(self.step) + "]}"
  def __repr__(self): return self.__str__()

def computeExpression(exp_map, i, typ):
  if   typ == "LHS": return exp_map[i][1]
  elif typ == "RHS": return exp_map[i][3]
  else: print('invalid type'); assert(False)


class ArrayVisitor(ast.NodeVisitor):
  """ Visit array assignments / uses to gather
      information to use in array dependence
      analysis within a For loop """
  def __init__(self, _newLoopVar, _allLoopVars):
    self.arrays = []
    self.loopVars = _allLoopVars + [_newLoopVar]
    self.arrayAccesses = []
    self.arrayWrites = []
  
  def visit_For(self, node):
    cprint(node, "Nested for found")
    global mynode1
    mynode1 = node

    loop_var_id, iter_name, iter_args = node.target.id, node.iter.func.id, node.iter.args
    iter_start, iter_end = iter_args[0], iter_args[1]

    assert(len(iter_args) in [1,2]) # TODO: add 3 for step argument
    assert(iter_name == "xrange" or iter_name == "range")

    next_depth = self.loopVars[-1].depth + 1 # going one loop deeper

    newLoopVar = Iterator(loop_var_id, iter_start, iter_end, next_depth)
    newArrVisitor = ArrayVisitor(newLoopVar, self.loopVars)
    for subnode in node.body:
      newArrVisitor.visit(subnode)

  def visit_Assign(self, node):
    global LHS, RHS, hi, mynode, allAccesses
    cprint(node, "Assign found")
    mynode = node

    LHS = node.targets[0].slice.value
    RHS = node.value.slice.value

    left = node.targets[0]
    left_array_name, left_indexing_exp, left_access_type = left.value.id, left.slice.value, "WRITE"
    arrAccessWrite = ArrayAccess(left_array_name, left_indexing_exp, left_access_type, deepcopy(self.loopVars))
    print arrAccessWrite

    right = node.value
    right_array_name, right_indexing_exp, right_access_type = right.value.id, right.slice.value, "READ"
    arrAccessRead = ArrayAccess(right_array_name, right_indexing_exp, right_access_type, deepcopy(self.loopVars))

    allWriteAccesses += [arrAccessWrite]
    allAccesses += [ArrAccessWrite, arrAccessRead]
    """
    for writeAccess in allWriteAccesses:
      writeDepth = len(writeAccess.iterators) - 1
      otherDepth = len(access.iterators) - 1

      # Check if write affects other access
      #   i.e. on the same or deeper depth
      if writeDepth >= otherDepth:
    """
    """
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
    """

class OutermostForLoopVisitor(ast.NodeVisitor):
  """ Visit all outermost for loops in program """
  def visit(self, node):
    if isinstance(node, ast.For):
      cprint(node, "For found")

      loop_var_id, iter_name, iter_args = node.target.id, node.iter.func.id, node.iter.args
      iter_start, iter_end = iter_args[0], iter_args[1]
      assert(len(iter_args) in [1,2]) # TODO: add 3 for step argument
      assert(iter_name == "xrange" or iter_name == "range")

      depth = 0
      loopVar = Iterator(loop_var_id, iter_start, iter_end, depth)
      arrVisitor = ArrayVisitor(loopVar, [])
      for subnode in node.body:
        arrVisitor.visit(subnode)

    else:
      self.generic_visit(node) # keep searching for for loops

  """
  def visit_Assign(self, node):
    print "Assign found"
  def visit_Return(self, node):
    print "Return found"
  """

tree = ast.parse(program)

#print "####\n", ast.dump(tree), "####\n"
allAccesses = []
visitor = OutermostForLoopVisitor()
for node in tree.body:
  visitor.visit(node)
  print "OUT"*5


writeAccesses = []
for access in allAccesses:
  if access.access_type == "WRITE":
    writeAccesses.append(access)

print writeAccesses
for writeAccess in writeAccesses:
  for access in allAccesses:
    writeDepth = len(writeAccess.iterators) - 1
    otherDepth = len(access.iterators) - 1

    # Check if write affects other access
    #   i.e. on the same or deeper depth
    #if writeDepth >= otherDepth:




