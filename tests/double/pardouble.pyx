
import cython
from cython import boundscheck, wraparound
from cython.parallel import prange, parallel
from libc.stdlib cimport malloc, free

def myfn():
  A = [None]*2000
  B = [None]*2000

  cdef int cyi
  cdef int cyj
  cdef int *cyA = <int *>malloc(len(A)*cython.sizeof(int))
  cdef int *cyB = <int *>malloc(len(B)*cython.sizeof(int))
  with nogil, parallel(num_threads=4):    
    for cyi in prange(0, 100):
        cyA[(cyi + 0)] = 13
        for cyj in prange(0, 100):
            cyB[(cyi + cyj)] = cyA[(cyi + 100)]



myfn()
