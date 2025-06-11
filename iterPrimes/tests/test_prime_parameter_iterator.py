import unittest
import sys
import os
from itertools import islice

# This assumes tests might be run from the project root

from iterPrimes.prime_parameter_iterator import PrimeParameterIterator

class TestPrimeParameterIterator(unittest.TestCase):
    def test_init_valid(self):
        it = PrimeParameterIterator(num_parameters=2, first_prime=3)
        self.assertEqual(it.num_parameters, 2)
        self.assertEqual(it.first_prime, 3)
        self.assertIsNone(it.max_generated_lists)

    def test_init_invalid_num_parameters(self):
        with self.assertRaises(ValueError):
            PrimeParameterIterator(num_parameters=-1)

    def test_num_parameters_zero(self):
        # Default max_generated_lists for num_parameters=0 is 1
        it = PrimeParameterIterator(num_parameters=0, first_prime=3)
        self.assertEqual(next(it), [])
        with self.assertRaises(StopIteration):
            next(it)

        it_max_2 = PrimeParameterIterator(num_parameters=0, first_prime=3, max_generated_lists=2)
        self.assertEqual(next(it_max_2), [])
        self.assertEqual(next(it_max_2), [])
        with self.assertRaises(StopIteration):
            next(it_max_2)

        it_max_0 = PrimeParameterIterator(num_parameters=0, first_prime=3, max_generated_lists=0)
        with self.assertRaises(StopIteration):
            next(it_max_0)


    def test_iteration_num_params_1(self):
        it = PrimeParameterIterator(num_parameters=1, first_prime=3, max_generated_lists=5)
        # Expected: (Round 1, P=[3]): [3]
        #           (Round 2, P=[3,5]): [3], [5]
        #           (Round 3, P=[3,5,7]): [3], [5] (stops at 5th overall list)
        expected_sequence = [[3], [3], [5], [3], [5]]
        actual_sequence = list(it)
        self.assertEqual(actual_sequence, expected_sequence)

    def test_iteration_num_params_2_max_lists_6(self):
        it = PrimeParameterIterator(num_parameters=2, first_prime=3, max_generated_lists=6)
        # Expected: (R1, P=[3]): [3,3] (1 list)
        #           (R2, P=[3,5]): [3,3], [3,5], [5,3], [5,5] (4 lists)
        #           (R3, P=[3,5,7]): [3,3] (1 list, total 1+4+1 = 6)
        expected_sequence = [
            [3,3],
            [3,3], [3,5], [5,3], [5,5],
            [3,3]
        ]
        actual_sequence = list(it)
        self.assertEqual(actual_sequence, expected_sequence)

    def test_iteration_num_params_2_max_lists_1(self):
        it = PrimeParameterIterator(num_parameters=2, first_prime=3, max_generated_lists=1)
        expected_sequence = [[3,3]]
        actual_sequence = list(it)
        self.assertEqual(actual_sequence, expected_sequence)

    def test_iteration_num_params_3_small_max(self):
        it = PrimeParameterIterator(num_parameters=3, first_prime=3, max_generated_lists=2)
        # Expected: (R1, P=[3]): [3,3,3]
        #           (R2, P=[3,5]): [3,3,3] (stops at 2nd overall list)
        expected_sequence = [[3,3,3], [3,3,3]]
        actual_sequence = list(it)
        self.assertEqual(actual_sequence, expected_sequence)

    def test_iteration_max_generated_lists_zero(self):
        it = PrimeParameterIterator(num_parameters=2, first_prime=3, max_generated_lists=0)
        expected_sequence = []
        actual_sequence = list(it)
        self.assertEqual(actual_sequence, expected_sequence)

    def test_yield_primes_integration_start_at_non_prime(self):
        # Iterator should correctly use yield_primes which starts with the next actual prime
        it = PrimeParameterIterator(num_parameters=1, first_prime=4, max_generated_lists=3)
        # Expected: (R1, P=[5]): [5]
        #           (R2, P=[5,7]): [5], [7]
        expected_sequence = [[5], [5], [7]]
        self.assertEqual(list(it), expected_sequence)

if __name__ == '__main__':
    unittest.main()
