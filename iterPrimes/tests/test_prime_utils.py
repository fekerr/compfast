import unittest
import sys
import os
from itertools import islice

# This assumes tests might be run from the project root or 'iterPrimes/tests'

from iterPrimes.prime_utils import yield_primes, _is_prime

class TestPrimeUtils(unittest.TestCase):
    def test_is_prime_function(self):
        self.assertFalse(_is_prime(0))
        self.assertFalse(_is_prime(1))
        self.assertTrue(_is_prime(2))
        self.assertTrue(_is_prime(3))
        self.assertFalse(_is_prime(4))
        self.assertTrue(_is_prime(5))
        self.assertFalse(_is_prime(6))
        self.assertTrue(_is_prime(7))
        self.assertFalse(_is_prime(9))
        self.assertTrue(_is_prime(11))
        self.assertTrue(_is_prime(13))
        self.assertFalse(_is_prime(15))
        self.assertTrue(_is_prime(23))
        self.assertTrue(_is_prime(29))
        # Test a larger prime
        self.assertTrue(_is_prime(7919)) # 1000th prime
        self.assertFalse(_is_prime(7920))


    def test_yield_primes_start_default(self):
        gen = yield_primes() # Starts at 2
        expected_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.assertEqual(list(islice(gen, 10)), expected_primes)

    def test_yield_primes_start_at_prime(self):
        gen = yield_primes(start_prime=7)
        expected_primes = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
        self.assertEqual(list(islice(gen, 10)), expected_primes)

    def test_yield_primes_start_at_composite(self):
        gen = yield_primes(start_prime=10)
        expected_primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
        self.assertEqual(list(islice(gen, 10)), expected_primes)

    def test_yield_primes_start_at_negative_or_one(self):
        gen = yield_primes(start_prime=-5) # Should start at 2
        self.assertEqual(next(gen), 2)
        gen = yield_primes(start_prime=0) # Should start at 2
        self.assertEqual(next(gen), 2)
        gen = yield_primes(start_prime=1) # Should start at 2
        self.assertEqual(next(gen), 2)


if __name__ == '__main__':
    unittest.main()
