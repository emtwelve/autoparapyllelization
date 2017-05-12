
import cython
from cython import boundscheck, wraparound
from cython.parallel import prange, parallel
from libc.stdlib cimport malloc, free

A = []*10
for i in xrange(0, 5):
  C[i+0] = C[i+0]
  for j in xrange(0,  5):
    A[i+11110] = B[i+j]
    A[i+12110] = B[j+i]
    for k in xrange(3, 8):
      A[i+j+k] = A[j+i+k]

  for m in xrange(2000,2001):
    A[m+0] = A[i+0]

  for n in xrange(10,15):
    C[n+0] = A[i+0]
    for q in xrange(13,15):
      C[q+i] = C[n+i]

