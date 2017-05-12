
import cython
from cython import boundscheck, wraparound
from cython.parallel import prange, parallel
from libc.stdlib cimport malloc, free
def looping_fn(hi):
  A = []*10
  B = []*10
  for i in xrange(0, 5):
    A[i+5] = A[i+0]
    B[i+0] = B[i+4]
  return A
