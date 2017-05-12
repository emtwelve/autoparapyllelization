
import cython
from cython import boundscheck, wraparound
from cython.parallel import prange, parallel
from libc.stdlib cimport malloc, free
def looping_fn(hi):
  A = []*10
  B = []*10
  cdef int cyi
  cdef int *cyA = <int *>malloc(len(A)*cython.sizeof(int))
  cdef int *cyB = <int *>malloc(len(B)*cython.sizeof(int))
  with nogil, parallel(num_threads=4):    
    for cyi in prange(0, 5):
        cyA[(cyi + 5)] = cyA[(cyi + 0)]
        cyB[(cyi + 0)] = cyB[(cyi + 5)]
  return A
