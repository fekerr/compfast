"""
Tests for the prime number generation functions in prime_minimal_branching_workload.

This module contains tests for:
- `simple_sieve`: For generating primes up to a small limit.
- `find_primes_in_segment`: For finding primes within a specific numerical range
  using a list of base primes.
"""
import sys
import os
import math

# Adjust the Python path to include the root directory
# This allows direct execution of the test script and importing from the parent 'workloads' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from workloads.prime_minimal_branching_workload import simple_sieve, find_primes_in_segment

# --- Tests for simple_sieve ---

def test_simple_sieve_basic():
  """
  Tests `simple_sieve` with common small inputs.
  """
  assert simple_sieve(10) == [2, 3, 5, 7], "Test Case 1: Primes up to 10"
  assert simple_sieve(20) == [2, 3, 5, 7, 11, 13, 17, 19], "Test Case 2: Primes up to 20"

def test_simple_sieve_edge_cases():
  """
  Tests `simple_sieve` with edge cases like limits 0, 1, and 2.
  """
  assert simple_sieve(2) == [2], "Test Case 3: Primes up to 2"
  assert simple_sieve(1) == [], "Test Case 4: Primes up to 1"
  assert simple_sieve(0) == [], "Test Case 5: Primes up to 0"
  # simple_sieve handles negative inputs by returning [], which is fine.
  # For limit < 2, it should return empty or [2] if limit is 2.
  # The current implementation of simple_sieve in the workload has:
  # if limit >= 0: is_prime[0] = False
  # if limit >= 1: is_prime[1] = False
  # This implies it expects non-negative limit.
  # Let's assume non-negative inputs based on typical sieve usage.

# --- Tests for find_primes_in_segment ---

def test_find_primes_in_segment_basic():
  """
  Tests `find_primes_in_segment` with typical segments and base primes.
  """
  base_primes_sqrt_100 = simple_sieve(int(math.sqrt(100))) # [2, 3, 5, 7]
  assert base_primes_sqrt_100 == [2, 3, 5, 7]

  # Test segment [10, 30]
  # Primes: 11, 13, 17, 19, 23, 29
  assert find_primes_in_segment(10, 30, base_primes_sqrt_100) == [11, 13, 17, 19, 23, 29], \
    "Test Case 1: Segment [10, 30]"

  # Test segment [90, 100]
  # Primes: 97
  assert find_primes_in_segment(90, 100, base_primes_sqrt_100) == [97], \
    "Test Case 2: Segment [90, 100]"

def test_find_primes_in_segment_no_primes():
  """
  Tests `find_primes_in_segment` for a segment expected to contain no primes.
  """
  base_primes_sqrt_30 = simple_sieve(int(math.sqrt(30))) # [2, 3, 5]
  assert base_primes_sqrt_30 == [2, 3, 5]

  # Segment [24, 26] contains 24 (2*12), 25 (5*5), 26 (2*13). No primes.
  assert find_primes_in_segment(24, 26, base_primes_sqrt_30) == [], \
    "Test Case 3: Segment [24, 26] (no primes)"

def test_find_primes_in_segment_small_segment():
  """
  Tests `find_primes_in_segment` with a very small segment.
  """
  base_primes_sqrt_10 = simple_sieve(int(math.sqrt(10))) # [2, 3]
  assert base_primes_sqrt_10 == [2, 3]

  # Segment [8, 10] contains 8, 9, 10. No primes.
  assert find_primes_in_segment(8, 10, base_primes_sqrt_10) == [], \
    "Test Case 4: Segment [8, 10] (no primes)"

def test_find_primes_in_segment_with_base_prime():
    """
    Tests if a base prime itself is correctly identified if it falls within a segment,
    especially when segment_low is small.
    """
    base_primes_up_to_5 = [2, 3, 5] # sqrt(approx 30)
    # Segment [2, 10]
    # Expected: 2, 3, 5, 7
    # The find_primes_in_segment should correctly handle this.
    # Its logic: for p in base_primes: current_multiple = max(p*p, ceil(low/p)*p)
    # if p=2, low=2: current_multiple = max(4, ceil(2/2)*2=2) = 4. Marks 4,6,8,10
    # if p=3, low=2: current_multiple = max(9, ceil(2/3)*3=3) = 9. Marks 9
    # if p=5, low=2: current_multiple = max(25, ceil(2/5)*5=5) = 25. (too high)
    # is_prime_segment for [2,3,4,5,6,7,8,9,10] (len 9)
    # Indices:         0,1,2,3,4,5,6,7,8
    # Initial:         T,T,T,T,T,T,T,T,T
    # After p=2 marks: T,T,F,T,F,T,F,T,F (4,6,8,10 are at indices 2,4,6,8)
    # After p=3 marks: T,T,F,T,F,T,F,F,F (9 is at index 7)
    # Result: 2,3,5,7 (numbers 2,3,5,7 at indices 0,1,3,5)
    assert find_primes_in_segment(2, 10, base_primes_up_to_5) == [2, 3, 5, 7]

def test_find_primes_in_segment_edge_case_one():
    """
    Tests behavior when segment includes 1.
    """
    base_primes_up_to_3 = [2, 3] # sqrt(approx 10)
    # Segment [0, 5]
    # Expected: 2, 3, 5
    # num > 1 check in find_primes_in_segment should handle 0 and 1 correctly.
    assert find_primes_in_segment(0, 5, base_primes_up_to_3) == [2, 3, 5]

def test_find_primes_in_segment_start_with_base_prime_square():
    """
    Tests a segment that starts exactly at the square of a base prime.
    """
    base_primes = [2,3,5,7]
    # Segment [49, 60] (7*7=49)
    # Expected: 53, 59
    assert find_primes_in_segment(49, 60, base_primes) == [53, 59]

def test_find_primes_in_segment_empty_base_primes():
    """
    Tests behavior if base_primes list is empty (e.g., sieving up to N < 4).
    This scenario shouldn't really happen if simple_sieve(sqrt_n) is called correctly,
    as sqrt_n would be < 2, and simple_sieve would return [].
    The segmented sieve logic usually assumes base_primes are available.
    If base_primes is empty, find_primes_in_segment should effectively treat all numbers in segment as prime.
    """
    # Segment [2, 10], no base primes means all are considered prime by find_primes_in_segment's marking loop.
    # The collection loop `if is_prime_segment[i]: if num > 1: primes_in_segment.append(num)`
    # would then add all numbers > 1 in the segment.
    assert find_primes_in_segment(2, 10, []) == [2,3,4,5,6,7,8,9,10] # This is the expected behavior of find_primes_in_segment in isolation
    # However, the overall segmented_sieve_workload handles N < 4 correctly, so this test
    # is more about the unit behavior of find_primes_in_segment.
    # The overall segmented_sieve_workload would not call find_primes_in_segment if sqrt_n < 2.
    # If N is, say, 3, sqrt_N is 1. simple_sieve(1) is [].
    # segmented_sieve_workload has:
    #   if n_limit <= sqrt_n: return # (all_primes from simple_sieve is returned)
    # For N=3, sqrt_n=1. 3 <= 1 is false.
    # current_low = sqrt_n + 1 = 2. segment_high = min(2+segment_size-1, 3)
    # It would call find_primes_in_segment(2, 3, [])
    # This would return [2,3]. Then all_primes (initially []) extends with [2,3]. Correct.
    assert find_primes_in_segment(2, 3, []) == [2,3]
    assert find_primes_in_segment(0, 1, []) == [] # Due to num > 1 check.
