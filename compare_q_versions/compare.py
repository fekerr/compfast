import sys
import os

# Adjust Python path to find sibling directories (iterPrimes, q_alpha, quaternion_explorer)
# This assumes 'compare_q_versions' is at the same level as those directories.
# Get the parent directory of the current script's directory (compare_q_versions)
# This should be the project root if compare_q_versions is a top-level dir.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from iterPrimes.prime_parameter_iterator import PrimeParameterIterator
from q_alpha.gaussian_int_quaternion import GaussianIntQuaternion
# Assuming the original quaternion class is in quaternion_explorer/quaternions.py
# And its name is Quaternion. Let's alias it for clarity.
from quaternion_explorer.quaternions import Quaternion as OriginalQuaternion
# We might also need IntegerGaussian if we interact with q_alpha's components directly
from q_alpha.integer_gaussian import IntegerGaussian


def run_comparison(num_param_sets_to_generate: int = 5):
    """
    Generates parameters, instantiates both quaternion types,
    and prints their properties and results of some operations for comparison.
    """
    print(f"Running comparison for {num_param_sets_to_generate} sets of parameters.\n")

    # Iterators for parameters
    # For GaussianIntQuaternion (q_alpha version), needs 8 integer parameters
    iter_giq = PrimeParameterIterator(num_parameters=8, first_prime=3, max_generated_lists=num_param_sets_to_generate * 2) # *2 for pairs for multiplication

    # For OriginalQuaternion (quaternion_explorer version), needs 4 integer parameters
    iter_oq = PrimeParameterIterator(num_parameters=4, first_prime=3, max_generated_lists=num_param_sets_to_generate * 2) # *2 for pairs

    for i in range(num_param_sets_to_generate):
        print(f"--- Comparison Set {i+1} ---")

        try:
            # Parameters for GaussianIntQuaternion (GIQ)
            giq_params1 = next(iter_giq)
            giq_params2 = next(iter_giq)

            # Parameters for OriginalQuaternion (OQ)
            oq_params1 = next(iter_oq)
            oq_params2 = next(iter_oq)

        except StopIteration:
            print("Ran out of parameters from iterator sooner than expected. Stopping.")
            break

        # Instantiate GaussianIntQuaternions
        giq1 = GaussianIntQuaternion(*giq_params1)
        giq2 = GaussianIntQuaternion(*giq_params2)

        # Instantiate OriginalQuaternions
        oq1 = OriginalQuaternion(*oq_params1)
        oq2 = OriginalQuaternion(*oq_params2)

        # 1. Compare String Representations
        print(f"  GIQ 1 ({giq_params1}): {str(giq1)}")
        print(f"  OQ  1 ({oq_params1}): {str(oq1)}")
        print(f"  GIQ 2 ({giq_params2}): {str(giq2)}")
        print(f"  OQ  2 ({oq_params2}): {str(oq2)}")
        print("-" * 20)

        # 2. Compare Multiplication Results
        try:
            giq_product = giq1 * giq2
            print(f"  GIQ Product (q1*q2): {str(giq_product)}")
        except Exception as e:
            print(f"  Error during GIQ multiplication: {e}")

        try:
            oq_product = oq1 * oq2
            print(f"  OQ  Product (q1*q2): {str(oq_product)}")
        except Exception as e:
            print(f"  Error during OQ multiplication: {e}")
        print("-" * 20)

        # 3. Compare other properties/methods if applicable
        # GIQ has conjugate
        try:
            giq1_conj = giq1.conjugate()
            print(f"  GIQ 1 Conjugate: {str(giq1_conj)}")
        except Exception as e:
            print(f"  Error during GIQ conjugate: {e}")

        # OQ has norm_squared and is_prime
        try:
            oq1_norm_sq = oq1.norm_squared()
            oq1_is_prime = oq1.is_prime()
            print(f"  OQ  1 Norm_Sq: {oq1_norm_sq}, Is_Prime: {oq1_is_prime}")
        except Exception as e:
            print(f"  Error during OQ norm/prime check: {e}")

        print("\n" + "="*40 + "\n")


if __name__ == '__main__':
    # Ensure the script can find sibling packages when run directly
    # The sys.path modification at the top should handle this.
    # If running this file directly, and the top-level project dir is not in PYTHONPATH,
    # you might need to set PYTHONPATH explicitly or run as a module from the root:
    # python -m compare_q_versions.compare

    num_sets = 5
    print(f"Executing comparison script from: {os.getcwd()}")
    print(f"Python sys.path includes: {PROJECT_ROOT}")
    print(f"Attempting to run comparison for {num_sets} sets...")
    run_comparison(num_sets)
