import unittest
from unittest.mock import patch # mock_open not needed for this.
import sys
import os
import io # For capturing stdout

# Adjust path to import from quaternion_explorer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# main_worker imports generate_gaussian_primes and Quaternion directly.
# We need to ensure these are available or mocked if main_worker is imported.
# For this test, we'll mostly be testing functions within main_worker or its overall execution.
import main_worker
# from gaussian_primes import generate_gaussian_primes # Not strictly needed for these tests due to mocking
# from quaternions import Quaternion # Not strictly needed for these tests due to mocking

class TestMainWorker(unittest.TestCase):

    # This test directly tests the component extraction logic as used in main_worker.py
    def test_component_extraction_logic(self):
        # Scenario 1: Typical Gaussian primes
        gaussian_primes_tuples = [(1, 1), (0, 3), (1, 2)]
        # Expected components (non-zero, unique from x,y in (x,y)): {1, 3, 2} -> sorted [1, 2, 3]

        integer_components_set = set()
        for x, y in gaussian_primes_tuples:
            if x != 0: integer_components_set.add(x)
            if y != 0: integer_components_set.add(y)
        integer_components_list = sorted(list(integer_components_set))
        self.assertEqual(integer_components_list, [1, 2, 3])

        # Scenario 2: Gaussian primes that might only have one unique non-zero component value
        gaussian_primes_tuples_2 = [(0, 7), (7, 0)]
        integer_components_set_2 = set()
        for x, y in gaussian_primes_tuples_2:
            if x != 0: integer_components_set_2.add(x)
            if y != 0: integer_components_set_2.add(y)
        integer_components_list_2 = sorted(list(integer_components_set_2))
        self.assertEqual(integer_components_list_2, [7])

        # Scenario 3: Empty Gaussian primes list
        gaussian_primes_tuples_3 = []
        integer_components_set_3 = set()
        for x, y in gaussian_primes_tuples_3: # Loop won't run
            if x != 0: integer_components_set_3.add(x)
            if y != 0: integer_components_set_3.add(y)
        self.assertTrue(not integer_components_set_3, "Component set should be empty for no Gaussian primes")


    @patch('main_worker.generate_gaussian_primes')
    @patch('main_worker.Quaternion')
    @patch('main_worker.random.choice')
    def test_overall_run_small_numbers_smoke_test(self, mock_random_choice, MockQuaternion, mock_ggp):
        # Configure mocks
        mock_ggp.return_value = [(1, 1), (0, 3)] # Components will be {1, 3} -> sorted list [1,3]

        mock_quaternion_instance = MockQuaternion.return_value
        mock_quaternion_instance.is_prime.return_value = True # All generated quaternions are "prime"
        mock_quaternion_instance.norm_squared.return_value = 1 # Dummy norm for products

        mock_random_choice.return_value = 1 # All components a,b,c,d will be 1

        # Patch configuration constants IN THE CONTEXT of main_worker module for this test
        with patch('main_worker.GAUSSIAN_PRIME_NORM_SQ_LIMIT', 10), \
             patch('main_worker.NUM_QUATERNIONS_TO_GENERATE', 5):

            captured_output = io.StringIO()
            sys.stdout = captured_output

            main_worker.run_quaternion_operations()

            sys.stdout = sys.__stdout__
            output_str = captured_output.getvalue()

            self.assertIn("Generated 2 Gaussian primes", output_str)
            self.assertIn("Extracted 2 unique non-zero integer components: [1, 3]", output_str)
            self.assertIn("Generating 5 quaternions", output_str)
            self.assertIn("Found 5 prime quaternions out of 5 generated.", output_str)
            self.assertIn("Total pairwise products calculated: 50", output_str) # 5*5*2
            self.assertIn("Sum of the squared norms of these product quaternions: 50", output_str) # 50 * 1
            self.assertIn("Average squared norm of the product quaternions: 1.00", output_str)
            self.assertNotIn("Error:", output_str)
            self.assertNotIn("Warning:", output_str)

    @patch('main_worker.generate_gaussian_primes')
    def test_run_no_gaussian_primes(self, mock_ggp):
        mock_ggp.return_value = []

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main_worker.run_quaternion_operations()
        sys.stdout = sys.__stdout__

        output_str = captured_output.getvalue()
        self.assertIn("Error: No Gaussian primes generated.", output_str)
        self.assertNotIn("Step 2:", output_str)

    @patch('main_worker.generate_gaussian_primes')
    def test_run_no_integer_components(self, mock_ggp):
        mock_ggp.return_value = [(0,0)] # Invalid GP output to force no non-zero components

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main_worker.run_quaternion_operations()
        sys.stdout = sys.__stdout__

        output_str = captured_output.getvalue()
        self.assertIn("Error: No non-zero integer components could be extracted", output_str)
        self.assertNotIn("Step 3:", output_str)

    @patch('main_worker.generate_gaussian_primes')
    @patch('main_worker.Quaternion')
    @patch('main_worker.random.choice') # Need to mock random.choice as it's used before prime filtering
    def test_run_less_than_two_prime_quaternions(self, mock_choice, MockQuaternion, mock_ggp):
        mock_ggp.return_value = [(1,1)]
        mock_choice.return_value = 1 # Make all generated quaternions Q(1,1,1,1)

        mock_quaternion_instance = MockQuaternion.return_value
        # Make only one quaternion pass the is_prime() check
        mock_quaternion_instance.is_prime.side_effect = [True, False, False]

        with patch('main_worker.NUM_QUATERNIONS_TO_GENERATE', 3):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            main_worker.run_quaternion_operations()
            sys.stdout = sys.__stdout__
            output_str = captured_output.getvalue()

            self.assertIn("Found 1 prime quaternions out of 3 generated.", output_str)
            self.assertIn("Need at least two prime quaternions to perform pairwise multiplication. Skipping.", output_str)
            self.assertNotIn("Total pairwise products calculated:", output_str)


if __name__ == '__main__':
    unittest.main()
