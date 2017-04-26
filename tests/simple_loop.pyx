
def looping_fn(hi):
  A = []*10
  B = []*10
  for i in xrange(0, 5):
    A[i+5] = A[i+0]
    B[i+0] = B[i+4]
  return A