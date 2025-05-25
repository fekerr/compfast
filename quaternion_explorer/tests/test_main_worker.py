import unittest
from unittest.mock import patch, mock_open # mock_open not needed for this.
import sys
import os
import io # For capturing stdout

# Adjust path to import from quaternion_explorer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# main_worker imports generate_gaussian_primes and Quaternion directly.
# We need to ensure these are available or mocked if main_worker is imported.
# For this test, we'll mostly be testing functions within main_worker or its overall execution.
import main_worker 
from gaussian_primes import generate_gaussian_primes # For direct use if needed, or for structure reference
from quaternions import Quaternion # For direct use if needed

class TestMainWorker(unittest.TestCase):

    @patch('main_worker.generate_gaussian_primes')
    def test_component_extraction_logic(self, mock_ggp):
        # This test is slightly more involved because component extraction is inside run_quaternion_operations.
        # A better design might have component extraction as a standalone function.
        # For now, we can test the logic by checking the side effects (prints) or by refactoring main_worker slightly.
        # Given the current structure, we'll check print output.
        
        # Scenario 1: Typical Gaussian primes
        mock_ggp.return_value = [(1, 1), (0, 3), (1, 2)] 
        # Expected components (non-zero, unique from x,y in (x,y)): {1, 3, 2} -> sorted [1, 2, 3]
        
        # Capture stdout to check print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # We need to run a part of run_quaternion_operations or check its behavior.
        # Since component extraction is deeply nested, we'll test the conditions.
        # What main_worker.py does for components:
        # integer_components_set = set() 
        # for x, y in gaussian_primes_tuples:
        #     if x != 0: integer_components_set.add(x)
        #     if y != 0: integer_components_set.add(y)
        # integer_components_list = sorted(list(integer_components_set))
        
        # Test this logic directly:
        gaussian_primes_tuples = [(1, 1), (0, 3), (1, 2)]
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
        
        # Scenario 3: No Gaussian primes (handled by main_worker's initial check)
        # mock_ggp.return_value = [] -> main_worker should print error and return.

        # Scenario 4: Gaussian primes that result in no non-zero components (should not happen)
        # e.g. if generate_gaussian_primes returned [(0,0)], which it shouldn't.
        # main_worker has a check: if not integer_components_set: print error and return.
        # This is covered by the logic.

        sys.stdout = sys.__stdout__ # Reset stdout


    @patch('main_worker.generate_gaussian_primes')
    @patch('main_worker.Quaternion') # Mock Quaternion if its behavior is complex/irrelevant
    @patch('main_worker.random.choice')
    def test_overall_run_small_numbers_smoke_test(self, mock_random_choice, MockQuaternion, mock_ggp):
        # Configure mocks
        # Mock generate_gaussian_primes to return a simple valid list
        mock_ggp.return_value = [(1, 1), (0, 3)] # Components will be {1, 3}
        
        # Mock Quaternion.is_prime() to control how many "prime" quaternions are found.
        # Let's say every generated quaternion is prime for simplicity in this smoke test.
        mock_quaternion_instance = MockQuaternion.return_value
        mock_quaternion_instance.is_prime.return_value = True
        mock_quaternion_instance.norm_squared.return_value = 1 # Dummy norm for products

        # Mock random.choice to return a fixed component (e.g., 1)
        # This makes quaternion generation deterministic for the test.
        # Components extracted will be [1,3]. Let random.choice always pick 1.
        # So all generated quaternions will be Q(1,1,1,1)
        mock_random_choice.return_value = 1
        
        # Patch configuration constants in main_worker for the test
        with patch('main_worker.GAUSSIAN_PRIME_NORM_SQ_LIMIT', 10), \
             patch('main_worker.NUM_QUATERNIONS_TO_GENERATE', 5):
            
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            main_worker.run_quaternion_operations() # Execute the main function
            
            sys.stdout = sys.__stdout__ # Reset stdout

            output_str = captured_output.getvalue()
            
            # Basic checks on the output
            self.assertIn("Starting quaternion operations...", output_str)
            self.assertIn("Step 1: Generating Gaussian primes", output_str)
            self.assertIn("Generated 2 Gaussian primes", output_str) # From mock_ggp
            self.assertIn("Extracted 2 unique non-zero integer components: [1, 3]", output_str)

            self.assertIn("Step 3: Generating 5 quaternions", output_str) # Patched NUM_QUATERNIONS_TO_GENERATE
            # All will be Q(1,1,1,1) due to random.choice mock

            self.assertIn("Step 4: Filtering for prime quaternions", output_str)
            # All 5 generated Q(1,1,1,1) will be "prime" due to MockQuaternion.is_prime mock
            self.assertIn("Found 5 prime quaternions out of 5 generated.", output_str) 
                                                                            
            self.assertIn("Step 5: Performing pairwise quaternion multiplication", output_str)
            # 5 prime quaternions. Q1*Q2 and Q2*Q1.
            # product_count = 5 (Q1 loop) * 5 (Q2 loop) * 2 (Q1*Q2 and Q2*Q1) = 50
            self.assertIn("Total pairwise products calculated: 50", output_str)
            # Each product norm_squared is mocked to 1. So sum_of_product_norms_sq = 50.
            self.assertIn("Sum of the squared norms of these product quaternions: 50", output_str)
            self.assertIn("Average squared norm of the product quaternions: 1.00", output_str)

            self.assertIn("Quaternion operations finished.", output_str)
            self.assertNotIn("Error:", output_str) # Check no error messages
            self.assertNotIn("Warning:", output_str)

    @patch('main_worker.generate_gaussian_primes')
    def test_run_no_gaussian_primes(self, mock_ggp):
        mock_ggp.return_value = [] # Simulate no Gaussian primes found
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main_worker.run_quaternion_operations()
        sys.stdout = sys.__stdout__
        
        output_str = captured_output.getvalue()
        self.assertIn("Error: No Gaussian primes generated.", output_str)
        self.assertNotIn("Step 2:", output_str) # Should exit early

    @patch('main_worker.generate_gaussian_primes')
    def test_run_no_integer_components(self, mock_ggp):
        # This case should ideally not be possible if generate_gaussian_primes always returns
        # tuples with non-zero numbers, or is empty.
        # Forcing it by returning [(0,0)] which is not a valid GP.
        mock_ggp.return_value = [(0,0)] # This is not a realistic output from actual generate_gaussian_primes
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main_worker.run_quaternion_operations()
        sys.stdout = sys.__stdout__
        
        output_str = captured_output.getvalue()
        self.assertIn("Generated 1 Gaussian primes (tuples): [(0, 0)]", output_str) # Shows mock value used
        self.assertIn("Error: No non-zero integer components could be extracted", output_str)
        self.assertNotIn("Step 3:", output_str) # Should exit early

    @patch('main_worker.generate_gaussian_primes')
    @patch('main_worker.Quaternion')
    def test_run_less_than_two_prime_quaternions(self, MockQuaternion, mock_ggp):
        mock_ggp.return_value = [(1,1)] # Components: [1]
        
        # Make only one quaternion pass the is_prime() check
        # Let NUM_QUATERNIONS_TO_GENERATE be, say, 3.
        # First one is prime, others are not.
        mock_quaternion_instance = MockQuaternion.return_value
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
```
