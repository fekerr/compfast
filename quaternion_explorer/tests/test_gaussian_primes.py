import unittest
import sys
import os

# Adjust path to import from quaternion_explorer
# This assumes tests are run from the root of the repository or quaternion_explorer is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gaussian_primes import is_prime, is_gaussian_prime, generate_gaussian_primes

class TestGaussianPrimes(unittest.TestCase):

    # Tests for is_prime(n)
    def test_is_prime_positive_cases(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
        for p in primes:
            self.assertTrue(is_prime(p), f"{p} should be prime")

    def test_is_prime_negative_cases(self):
        non_primes = [0, 1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, -1, -2, -10]
        for np in non_primes:
            self.assertFalse(is_prime(np), f"{np} should not be prime")

    # Tests for is_gaussian_prime(a, b)
    def test_is_gaussian_prime_axis_primes(self):
        # Non-zero part p is prime and p % 4 == 3
        self.assertTrue(is_gaussian_prime(3, 0), "(3,0) should be a Gaussian prime")
        self.assertTrue(is_gaussian_prime(0, 3), "(0,3) should be a Gaussian prime")
        self.assertTrue(is_gaussian_prime(7, 0), "(7,0) should be a Gaussian prime")
        self.assertTrue(is_gaussian_prime(0, 7), "(0,7) should be a Gaussian prime")
        self.assertTrue(is_gaussian_prime(11, 0), "(11,0) should be a Gaussian prime")
        self.assertTrue(is_gaussian_prime(0, 11), "(0,11) should be a Gaussian prime")
        self.assertTrue(is_gaussian_prime(19, 0), "(19,0) should be a Gaussian prime")
        self.assertTrue(is_gaussian_prime(0, 23), "(0,23) should be a Gaussian prime")


    def test_is_gaussian_prime_axis_non_primes(self):
        # Cases where non-zero part is not p % 4 == 3 or not prime
        self.assertFalse(is_gaussian_prime(1, 0), "(1,0) is not GP (1 not prime or 1%4!=3)")
        self.assertFalse(is_gaussian_prime(0, 1), "(0,1) is not GP (1 not prime or 1%4!=3)")
        self.assertFalse(is_gaussian_prime(2, 0), "(2,0) is not GP (2%4!=3)")
        self.assertFalse(is_gaussian_prime(0, 2), "(0,2) is not GP (2%4!=3)")
        self.assertFalse(is_gaussian_prime(5, 0), "(5,0) is not GP (5%4!=3)")
        self.assertFalse(is_gaussian_prime(0, 5), "(0,5) is not GP (5%4!=3)")
        self.assertFalse(is_gaussian_prime(6, 0), "(6,0) is not GP (6 not prime)")
        self.assertFalse(is_gaussian_prime(0, 9), "(0,9) is not GP (9 not prime)")
        self.assertFalse(is_gaussian_prime(13,0), "(13,0) is not GP (13%4!=3)")

    def test_is_gaussian_prime_norm_is_prime(self):
        # Neither a nor b is zero, and a*a + b*b is prime
        self.assertTrue(is_gaussian_prime(1, 1), "(1,1) norm_sq=2 (prime), should be GP") # 1*1+1*1=2
        self.assertTrue(is_gaussian_prime(1, 2), "(1,2) norm_sq=5 (prime), should be GP") # 1*1+2*2=5
        self.assertTrue(is_gaussian_prime(2, 1), "(2,1) norm_sq=5 (prime), should be GP")
        self.assertTrue(is_gaussian_prime(2, 3), "(2,3) norm_sq=13 (prime), should be GP") # 2*2+3*3=13
        self.assertTrue(is_gaussian_prime(3, 2), "(3,2) norm_sq=13 (prime), should be GP")
        self.assertTrue(is_gaussian_prime(1, 4), "(1,4) norm_sq=17 (prime), should be GP") # 1*1+4*4=17
        self.assertTrue(is_gaussian_prime(4, 1), "(4,1) norm_sq=17 (prime), should be GP")
        self.assertTrue(is_gaussian_prime(2,5), "(2,5) norm_sq=29 (prime), should be GP")
        self.assertTrue(is_gaussian_prime(5,2), "(5,2) norm_sq=29 (prime), should be GP")


    def test_is_gaussian_prime_norm_is_not_prime(self):
        # Neither a nor b is zero, but a*a + b*b is not prime
        self.assertFalse(is_gaussian_prime(1, 3), "(1,3) norm_sq=10 (not prime)") # 1*1+3*3=10
        self.assertFalse(is_gaussian_prime(2, 2), "(2,2) norm_sq=8 (not prime)")   # 2*2+2*2=8
        self.assertFalse(is_gaussian_prime(2, 4), "(2,4) norm_sq=20 (not prime)") # 2*2+4*4=20
        self.assertFalse(is_gaussian_prime(3,3), "(3,3) norm_sq=18 (not prime)")

    def test_is_gaussian_prime_mixed_zeros(self):
        self.assertFalse(is_gaussian_prime(0, 0), "(0,0) is not a Gaussian prime")

    # Tests for generate_gaussian_primes(limit)
    def test_generate_gaussian_primes_small_limit(self):
        # Based on the worker's implementation of generate_gaussian_primes
        # which stores unique tuple(sorted((x,y))) for x,y > 0
        # and (x,0) or (0,y) for axis primes.
        # For limit_on_norm_squared = 10:
        # (1,1) -> norm_sq=2
        # (1,2) -> norm_sq=5 (also covers (2,1))
        # (0,3) -> norm_sq=9 (3%4==3)
        # (3,0) -> norm_sq=9 (3%4==3)
        # (2,2) -> norm_sq=8 (not GP)
        expected = sorted([(0, 3), (1, 1), (1, 2), (3, 0)])
        result = generate_gaussian_primes(10)
        self.assertEqual(result, expected, "Test with limit 10 failed")

        self.assertEqual(generate_gaussian_primes(1), [], "Test with limit 1 failed")
        self.assertEqual(generate_gaussian_primes(0), [], "Test with limit 0 failed")
        # For limit 2, only (1,1) has norm_sq 2.
        self.assertEqual(generate_gaussian_primes(2), sorted([(1,1)]), "Test with limit 2 failed")


    def test_generate_gaussian_primes_properties(self):
        limit = 50
        generated_primes = generate_gaussian_primes(limit)
        
        # Check for uniqueness (already handled by set in implementation, but verify list output)
        self.assertEqual(len(generated_primes), len(set(generated_primes)), "Generated list should be unique")
        
        # Check if sorted (as per implementation detail)
        self.assertEqual(generated_primes, sorted(generated_primes), "Generated list should be sorted")

        for p_tuple in generated_primes:
            a, b = p_tuple
            self.assertTrue(is_gaussian_prime(a, b), f"{p_tuple} generated by generate_gaussian_primes should be a Gaussian prime")
            norm_sq = a*a + b*b
            self.assertTrue(norm_sq <= limit, f"Norm squared of {p_tuple} is {norm_sq}, exceeds limit {limit}")

            # Check canonical form for x,y > 0
            if a > 0 and b > 0:
                self.assertTrue(a <= b, f"For x,y > 0, tuple {(a,b)} should be sorted (a <= b)")
            # Check for (0,0)
            self.assertNotEqual(p_tuple, (0,0), "(0,0) should not be in the list of Gaussian primes")


if __name__ == '__main__':
    unittest.main()
```
