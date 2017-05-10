
A = [None]*20
B = [None]*20
for i in xrange(0, 5):
  A[i+0] = 13
  for j in xrange(0,  5):
    B[i+j] = A[i+5]

print A
print B