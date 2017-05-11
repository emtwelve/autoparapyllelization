import cython
from cython import boundscheck, wraparound
from cython.parallel import prange, parallel
from libc.stdlib cimport malloc, free


def myfn():
  A = [None]*200000000
  B = [None]*200000000
  cdef int i, j
  cdef int *cyA = <int *>malloc(len(A)*cython.sizeof(int))
  cdef int *cyB = <int *>malloc(len(B)*cython.sizeof(int))
  
  from datetime import datetime
  startTime = datetime.now();

  cdef int i, j
  cdef int *cyA = <int *>malloc(len(A)*cython.sizeof(int))
  cdef int *cyB = <int *>malloc(len(B)*cython.sizeof(int))
  with nogil, parallel(num_threads=8):
    for i in prange(0, 1000, schedule='static'):
      cyA[i+0] = 13
      for j in xrange(0, 1000):
        cyB[i+j] = cyA[i+1000]


  print datetime.now() - startTime


myfn()