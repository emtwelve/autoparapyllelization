import ast
from copy import deepcopy
from sys import exit

from sys import argv
if len(argv) != 2:
    print "Need program to analyze as argument"
    assert(False)

program = open(argv[1], 'r').read()

print "####\n", program, "####"

# For identifying array accesses
UNIQUE_ID = 0

def cprint(node, s):
  """ Print s indented by node.col_offset """
  print " "*node.col_offset + s

######################################################
"""###################################################
AST Modifiers:
"""###################################################
######################################################
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

######################################################
"""###################################################
Expression map builders and wrappers:
"""###################################################
######################################################
def build_expression_map(v, exp):
  exp_map = []

  for i in xrange(v.lower, v.upper, v.step):
    _exp = deepcopy(exp)
    ReplaceWithConstant(i, v.id).visit(_exp)
    ast.fix_missing_locations(_exp)
    exp_val = eval(compile(ast.Expression(_exp), filename="<ast>", mode="eval"))
    exp_map += [(_LHS, LHS_val, _RHS, RHS_val)]

  return exp_map

## Deprecated...
def computeExpression(exp_map, i, typ):
  if   typ == "LHS": return exp_map[i][1]
  elif typ == "RHS": return exp_map[i][3]
  else: print('invalid type'); assert(False)

######################################################
"""###################################################
Expression and Subscript string building and printing:
"""###################################################
######################################################
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

######################################################
"""###################################################
ArrayAccess and Iterator class definitions:
"""###################################################
######################################################
class ArrayAccess(object):
  def __init__(self, _array_name, _indexing_exp, _access_type, _iterators, _lineno):
    self.array_name = _array_name
    self.access_type = _access_type
    self.indexing_exp = _indexing_exp
    self.iterators = _iterators
    self.lineno = _lineno
    global UNIQUE_ID
    self.unique_id = UNIQUE_ID
    UNIQUE_ID += 1
  def __str__(self):
    return "ACCESS_" + str(self.unique_id) + \
           "{" + \
              self.array_name + \
              "[" + buildExpressionString(self.indexing_exp) + "]" + \
              " " + self.access_type + " " + "line:"+str(self.lineno) + \
              " " + str(self.iterators) + "}"
  def __repr__(self):
    return self.__str__()

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

######################################################
"""###################################################
AST node visitor class definition:
"""###################################################
######################################################
class ArrayVisitor(ast.NodeVisitor):
  """ Visit array assignments / uses to gather
      information to use in array dependence
      analysis within a For loop """
  def __init__(self, _newLoopVar, _allLoopVars):
    self.arrays = []
    self.loopVars = _allLoopVars + [_newLoopVar]
    self.arrayAccesses = []
    self.arrayWrites = []
  
  # When finiding a for loop, get it its iterator,
  #   calculate one level deeper,
  #   and look for more array accesses
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

  # When finding an assignment statement,
  #   look for Subscripts and assign their array accesses
  #   to just the global write access list or both
  #   the aforementione list and the all accesses list
  def visit_Assign(self, node):
    global LHS, RHS, hi, mynode, allAccesses, allWriteAccesses
    cprint(node, "Assign found")
    mynode = node

    LHS_accesses = []
    for subnode in ast.walk(node.targets[0]):
      print subnode
      if isinstance(subnode, ast.Subscript):
        print 'hello'
        mynode = subnode
        LHS_accesses.append(subnode)

    print "YO man"
    RHS_accesses = []
    for subnode in ast.walk(node.value):
      print subnode
      if isinstance(subnode, ast.Subscript):
        RHS_accesses.append(subnode)

    for left in LHS_accesses:
      left_array_name, left_indexing_exp, left_access_type = \
        left.value.id, left.slice.value, "WRITE"
      arrAccessWrite = \
        ArrayAccess(left_array_name, left_indexing_exp,
                    left_access_type, deepcopy(self.loopVars),
                    left.lineno)
      allWriteAccesses += [arrAccessWrite]
      allAccesses += [arrAccessWrite]

    for right in RHS_accesses:
      right_array_name, right_indexing_exp, right_access_type = \
        right.value.id, right.slice.value, "READ"
      arrAccessRead = \
        ArrayAccess(right_array_name, right_indexing_exp,
                    right_access_type, deepcopy(self.loopVars),
                    right.lineno)
      allAccesses += [arrAccessRead]
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


def DP(doflsts):
  # Base:
  if len(doflsts) == 1:
    d_lst = []
    for itr, vals in doflsts.items():
      for val in vals:
        d_lst.append({itr:val})
    return  d_lst

  # Recurse:
  else:
    key = doflsts.keys()[0]
    lst = doflsts[key]
    del doflsts[key]
    d_lst = DP(doflsts)
    new_d_lst = []
    for val in lst:
      for ds in d_lst:
        new_d = deepcopy(ds)
        new_d[key] = val
        new_d_lst.append(new_d)
    return new_d_lst

def getEvaluatedIdxAccesses(access):
  loopIters = access.iterators

  # Generate all possible accesses to the write:
  doflsts = {}
  for loopIter in loopIters:
    doflsts[loopIter.id] = range(loopIter.lower, loopIter.upper, loopIter.step)
  iter_to_vals = DP(doflsts)

  # Create list of this expression evaluated at all points:
  evaluated_expressions = []
  for iter_to_val in iter_to_vals:
    expression = deepcopy(access.indexing_exp)
    for itrid, val in iter_to_val.items(): # {i:0, j:0, k:0} mapping

      ReplaceWithConstant(val, itrid).visit(expression)
      ast.fix_missing_locations(expression)

    evaluated_expressions.append(expression)

  # Generate possible values of access to the array:
  evaluated_idx_accesses = []
  for eval_exp in evaluated_expressions:
    evaluated_idx_accesses.append(eval(compile(ast.Expression(eval_exp), filename="<ast>", mode="eval")))

  return evaluated_idx_accesses

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

if __name__ == "__main__":
  tree = ast.parse(program)
  #print "####\n", ast.dump(tree), "####\n"

  # Find all array accesses:
  allWriteAccesses = []
  allAccesses = []
  visitor = OutermostForLoopVisitor()
  for node in tree.body:
    visitor.visit(node)
    #print "~"*5


  print allWriteAccesses
  for writeAccess in allWriteAccesses:
    for otherAccess in allAccesses:
      # Check if we are accessing the same array,
      #   otherwise no dependencies possible:
      if writeAccess.array_name == otherAccess.array_name and \
         writeAccess.unique_id != otherAccess.unique_id:
        print "hello"
        writeEvaluatedAccesses = set(getEvaluatedIdxAccesses(writeAccess))
        otherEvaluatedAccesses = set(getEvaluatedIdxAccesses(otherAccess))
        if len(writeEvaluatedAccesses.intersection(otherEvaluatedAccesses)) != 0:
          print "Array accesses:\n\t", writeAccess, "and\n\t", otherAccess, "conflict"



