
import cython
from cython import boundscheck, wraparound
from cython.parallel import prange, parallel
from libc.stdlib cimport malloc, free
import time

def hello():
    start = time.time()
    print "hello world"
    end = time.time()
    print end - start


