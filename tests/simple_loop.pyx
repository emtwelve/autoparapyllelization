
def looping_fn(hi):
  A = []*10
  for i in range(10):
    A[i] = i

  for j in range(5):
    A[5-j] = j

  return A