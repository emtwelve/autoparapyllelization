
import cython
from cython import boundscheck, wraparound
from cython.parallel import prange, parallel
from libc.stdlib cimport malloc, free

def matmult3x3(A, B):
    C = [0]*len(A)

    for i in range(0,3):
        for j in range(0,3):
            for k in range(0,3):
                C[i*3+j] += A[i*3+k] * B[k*3+j]

    print C
    return C

matmult3x3([3,3,3,3,3,3,3,3,3],[1,3,1,3,1,3,1,3,1])
