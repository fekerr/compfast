"""
Segmented Sieve of Eratosthenes Workload

This script implements the Segmented Sieve of Eratosthenes algorithm to find
all prime numbers up to a given limit 'N'. It is designed to be more memory
efficient than a simple sieve for large N by processing numbers in segments.
The key functions are profiled for time and memory usage.
"""
import sys
import os
import math

# Adjust the Python path to include the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decorators.profiling import time_it, memory_profile_it

@time_it
@memory_profile_it
def simple_sieve(limit: int) -> list[int]:
  """
  Generates primes up to a given limit using a simple Sieve of Eratosthenes.

  This function is used to find base primes up to sqrt(N) for the segmented sieve.

  Args:
    limit: The upper bound for finding primes.

  Returns:
    A list of prime numbers up to 'limit'.
  """
  primes = []
  is_prime = [True] * (limit + 1)
  if limit >= 0:
    if limit >= 0: is_prime[0] = False
    if limit >= 1: is_prime[1] = False

  for p in range(2, limit + 1):
    if is_prime[p]:
      primes.append(p)
      for i in range(p * p, limit + 1, p):
        is_prime[i] = False
  return primes

@time_it
@memory_profile_it
def find_primes_in_segment(segment_low: int, segment_high: int, base_primes: list[int]) -> list[int]:
  """
  Finds prime numbers within a given segment [segment_low, segment_high].

  It uses the 'base_primes' (primes up to sqrt(N)) to mark non-primes in the segment.

  Args:
    segment_low: The lower bound of the current segment.
    segment_high: The upper bound of the current segment.
    base_primes: A list of prime numbers up to sqrt of the overall limit N.

  Returns:
    A list of prime numbers found within the segment.
  """
  segment_size = segment_high - segment_low + 1
  is_prime_segment = [True] * segment_size
  primes_in_segment = []

  for p in base_primes:
    # Find the smallest multiple of p that is >= segment_low
    # (p - (segment_low % p)) % p gives the offset from segment_low to the first multiple of p
    # If segment_low is a multiple of p, start_multiple_offset will be 0.
    # Otherwise, it will be p minus the remainder of segment_low / p.
    # The first multiple is then segment_low + start_multiple_offset.
    # A simpler way: start = ceil(segment_low / p) * p
    start_multiple = math.ceil(segment_low / p) * p

    # If the prime itself is in the current segment and is the start_multiple,
    # ensure it's not marked off if segment_low <= p < start_multiple.
    # However, this sieve method correctly handles it: p is marked if it's a multiple of a *smaller* prime.
    # If p itself is the start_multiple, it should only be marked if it's not p.
    # This implies we should start marking from p*p or the first multiple in range.
    # For segmented sieve, we mark multiples of base_primes.
    # The smallest multiple of p to mark is p*p. If p*p > segment_high, no multiples of p are in this segment (unless p itself is).
    # If p*p < segment_low, the first multiple to mark is the first multiple >= segment_low.

    if p * p > segment_high: # Optimization: if p*p is already beyond the segment, larger multiples will also be.
        continue

    # Adjust start_multiple if it's less than p*p (as multiples less than p*p would have been sieved by smaller primes)
    # This also ensures that 'p' itself is not marked off if 'p' is in base_primes and also in the current segment.
    # Specifically, if segment_low <= p < start_multiple, we might miss p.
    # The start_multiple must be at least p*p OR the first multiple of p in the segment.
    # Let's use max(p*p, first multiple of p >= segment_low)

    current_multiple = max(p * p, start_multiple)

    # Mark multiples of p in the current segment
    for i in range(current_multiple, segment_high + 1, p):
      if i >= segment_low: # Ensure we are within the current segment
        is_prime_segment[i - segment_low] = False

  # Collect primes from the segment
  for i in range(segment_size):
    if is_prime_segment[i]:
      num = segment_low + i
      # Special case: 1 is not prime. Also, segment_low could be 0 or 1.
      if num > 1: # Ensure numbers are greater than 1
          primes_in_segment.append(num)

  return primes_in_segment

@time_it
@memory_profile_it
def segmented_sieve_workload(n_limit: int):
  """
  Orchestrates the Segmented Sieve of Eratosthenes to find primes up to n_limit.

  Args:
    n_limit: The upper bound for finding prime numbers.
  """
  if n_limit < 2:
    print(f"No primes found up to {n_limit}.")
    return

  sqrt_n = int(math.sqrt(n_limit))
  print(f"Calculating primes up to N = {n_limit}. Base primes up to sqrt(N) = {sqrt_n}.")

  base_primes = simple_sieve(sqrt_n)
  all_primes = list(base_primes) # Initialize with base primes

  # Segment size can be sqrt_n or a fixed value. Let's use sqrt_n, or a reasonable default.
  segment_size = max(sqrt_n, 10000) # Ensure a minimum segment size for very small N
  if n_limit <= sqrt_n : # If N is small, simple_sieve already found all primes
      print(f"Found {len(all_primes)} primes up to {n_limit}.")
      if all_primes:
          print(f"Last few primes: {all_primes[-5:]}")
      return


  # Start segmenting from sqrt_n + 1
  # The first number in the first segment is sqrt_n + 1 (or 2 if sqrt_n < 1)
  # However, base_primes already cover up to sqrt_n.
  # So, the first segment should start after sqrt_n.
  # The simple_sieve gives primes <= sqrt_n.
  # The main loop of segmented sieve should cover numbers > sqrt_n.

  # Correct starting point for segments
  current_low = sqrt_n + 1

  print(f"Using segment size: {segment_size}")

  while current_low <= n_limit:
    segment_high = min(current_low + segment_size - 1, n_limit)
    print(f"Processing segment: [{current_low}, {segment_high}]")

    # In find_primes_in_segment, numbers are added if is_prime_segment[i - segment_low] is True.
    # This means if segment_low = 0, index is i. if segment_low = 10, index is i-10.
    # segment_low cannot be 0 if it starts from sqrt_n + 1, unless sqrt_n = -1 (not possible).
    # Also, numbers like 0 and 1 should not be added. The check `if num > 1` in find_primes_in_segment handles this.

    primes_in_this_segment = find_primes_in_segment(current_low, segment_high, base_primes)
    all_primes.extend(primes_in_this_segment)

    current_low += segment_size

  print(f"\nTotal number of primes found up to {n_limit}: {len(all_primes)}")
  if len(all_primes) > 0:
    print(f"Last 10 primes: {all_primes[-10:]}")
  else:
    print("No primes found.")

if __name__ == "__main__":
  N_LIMIT = 1_000_000  # Example: 1 million
  # N_LIMIT = 100 # For quick testing
  print(f"Starting Segmented Sieve workload for N = {N_LIMIT}...")
  segmented_sieve_workload(N_LIMIT)
  print("Segmented Sieve workload finished.")
