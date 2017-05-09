
A = []*10
for i in xrange(0, 5):
  C[i] = C[i]
  for j in xrange(0,  5):
    B[j+i] = B[i+j]
    for k in xrange(3, 8):
      A[i+j+k] = A[j+i+k]

  for m in xrange(15,20):
    A[m] = A[i]

  for n in xrange(10,15):
    C[n] = A[i]
    for q in xrange(13,15):
      C[q+i] = C[n+i]
