
import cython
from cython import boundscheck, wraparound
from cython.parallel import prange, parallel
from libc.stdlib cimport malloc, free

A = [None]*1000
B = [None]*1000

# Loop 0: [ Parallelizable ]
cdef int cyi
cdef int cyj
cdef int *cyA = <int *>malloc(len(A)*cython.sizeof(int))
cdef int *cyB = <int *>malloc(len(B)*cython.sizeof(int))
with nogil, parallel(num_threads=4):  
  for cyi in prange(0, 100):
      cyA[(cyi + 0)] = 13
      for cyj in prange(0, 100):
          cyB[(cyi + cyj)] = cyA[(cyi + 100)]


# Loop 1: [ Parallelizable ]
with nogil, parallel(num_threads=4):  
  for cyi in prange(0, 100):
      cyA[(cyi + 0)] = cyB[(cyi + 0)]
      for cyj in prange(0, 100):
          cyB[(cyj + 100)] = cyA[(cyi + 100)]

# Loop 2: [ Not parallelizable ]
for i in xrange(0, 100):
  A[i+0] = B[i+0]
  for j in xrange(0, 100):
    B[j+100] = A[i+99]

"""
# Loop 3: [ Parallelizable ]
for i in xrange(0, 100):
  A[i+0] = B[i+0]
  for j in xrange(0, 100):
    for k in xrange(100, 110):
      B[j+100] = A[i+k]

# Loop 4: [ Not parallelizable ]
for i in xrange(0, 100):
  A[i+0] = B[i+0]
  for j in xrange(0, 100):
    for k in xrange(99, 109):
      B[j+100] = A[i+k]
"""

