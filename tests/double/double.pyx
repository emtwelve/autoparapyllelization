
def myfn():
  A = [None]*2000
  B = [None]*2000

  for i in xrange(0, 100):
    A[i+0] = 13
    for j in xrange(0, 100):
      B[i+j] = A[i+100]



myfn()