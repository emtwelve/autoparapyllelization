
import cython
from cython import boundscheck, wraparound
from cython.parallel import prange, parallel
from libc.stdlib cimport malloc, free

A = [None]*10
cdef int cyi
cdef int *cyA = <int *>malloc(len(A)*cython.sizeof(int))
with nogil, parallel(num_threads=4):  
  for cyi in prange(0, 5):
      cyA[(cyi + 5)] = cyA[(cyi + 0)]


