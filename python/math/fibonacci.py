def fib(n):
  if n < 2:
    return n
  a, b = 0, 1
  for _ in range(2, n):
    a, b = b, a + b
  return b