def fib(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Test the Fibonacci function
import unittest

class TestFibonacci(unittest.TestCase):
    def test_fibonacci(self):
        self.assertEqual(fib(10), 55)

if __name__ == '__main__':
    unittest.main()
