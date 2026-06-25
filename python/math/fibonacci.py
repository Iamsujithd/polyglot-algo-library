import functools

def fib(n):
    if n < 2: return n
    return functools.reduce(lambda x, _: x + fib(x + 1), range(n - 2), 0)
