
A = [None]*1000
B = [None]*1000

# Loop 0: [ Parallelizable ]
for i in xrange(0, 100):
  A[i+0] = 13
  for j in xrange(0, 100):
    B[i+j] = A[i+100]

# Loop 1: [ Parallelizable ]
for i in xrange(0, 100):
  A[i+0] = B[i+0]
  for j in xrange(0, 100):
    B[j+100] = A[i+100]

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
