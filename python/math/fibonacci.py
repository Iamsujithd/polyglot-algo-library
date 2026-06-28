
import math

def fib(n):
    a, b = 0, 1
    for _ in range(n-1):
        a, b = b, a+b
    return min(a, b)

# Test cases
if __name__ == '__main__':
    print(fib(10))
