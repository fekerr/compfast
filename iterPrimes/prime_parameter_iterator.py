from typing import List, Optional, Iterator
from iterPrimes.prime_utils import yield_primes

class PrimeParameterIterator:
    """
    Iterates through combinations of prime numbers for a specified number of parameters.
    The iteration proceeds by exhausting all combinations for a growing set of primes.
    For example, with num_parameters=2 and first_prime=3:
    1. Current primes set: [3]. Combinations: [3,3]. (1 list)
    2. Current primes set: [3,5]. Combinations: [3,3], [3,5], [5,3], [5,5]. (4 lists)
    3. Current primes set: [3,5,7]. Combinations: [3,3], [3,5], [3,7], [5,3], ..., [7,7]. (9 lists)
    And so on. The iterator yields these lists sequentially.
    """

    def __init__(self, num_parameters: int, first_prime: int = 3, max_generated_lists: Optional[int] = None):
        if num_parameters < 0:
            raise ValueError("Number of parameters must be non-negative.")

        self.num_parameters = num_parameters
        self.first_prime = first_prime
        self.max_generated_lists = max_generated_lists

        self._prime_generator = yield_primes(self.first_prime)
        self._primes_list: List[int] = []
        self._param_indices: List[int] = [0] * self.num_parameters
        self._generated_count = 0
        self._current_prime_base_size = 0

        if self.num_parameters == 0:
            if self.max_generated_lists is None: # Default to yielding one empty list then stopping
                self.max_generated_lists = 1
        else:
            # Initialize with the first prime to establish the first base set
            self._expand_prime_base()

    def _expand_prime_base(self):
        """Adds the next available prime to self._primes_list and resets indices for a new round of combinations."""
        try:
            next_p = next(self._prime_generator)
            self._primes_list.append(next_p)
            self._current_prime_base_size = len(self._primes_list)
            # Reset indices to start combinations with the new prime base
            self._param_indices = [0] * self.num_parameters
        except StopIteration:
            raise RuntimeError("Prime generator exhausted unexpectedly.")

    def __iter__(self) -> Iterator[List[int]]:
        return self

    def __next__(self) -> List[int]:
        if self.max_generated_lists is not None and self._generated_count >= self.max_generated_lists:
            raise StopIteration

        if self.num_parameters == 0:
            if self.max_generated_lists is None: # Should have been set in __init__
                 raise StopIteration # Or handle as per __init__'s default
            if self._generated_count < self.max_generated_lists:
                self._generated_count += 1
                return []
            else:
                raise StopIteration

        if not self._primes_list: # Should be initialized if num_parameters > 0
             raise StopIteration

        # Construct current result
        current_result = [self._primes_list[idx] for idx in self._param_indices]
        self._generated_count += 1

        # Increment indices for the next state (odometer style for current prime base)
        position_to_increment = self.num_parameters - 1
        while position_to_increment >= 0:
            self._param_indices[position_to_increment] += 1

            if self._param_indices[position_to_increment] < self._current_prime_base_size:
                # This position incremented successfully within the current prime base. Done.
                break
            else:
                # This position rolled over for the current prime base. Reset it.
                self._param_indices[position_to_increment] = 0
                if position_to_increment == 0:
                    # Leftmost position rolled over. All combinations for the current
                    # _current_prime_base_size are exhausted. Expand the base for the next round.
                    self._expand_prime_base()
                    # Indices are already reset by _expand_prime_base.
                    break
                else:
                    # Carry over to the next position to the left.
                    position_to_increment -= 1

        return current_result

if __name__ == '__main__':
    print("Testing PrimeParameterIterator(num_parameters=1, first_prime=3, max_generated_lists=5)")
    # Expected sequence for num_parameters=1:
    # Base [3] (size 1): Yields [3]. Next iter: expand base to [3,5], indices [0].
    # Base [3,5] (size 2): Yields [3]. Next iter: indices [1].
    # Base [3,5] (size 2): Yields [5]. Next iter: expand base to [3,5,7], indices [0].
    # Base [3,5,7] (size 3): Yields [3]. Next iter: indices [1].
    # Base [3,5,7] (size 3): Yields [5]. Next iter: indices [2]. (Stops due to max_generated_lists=5)
    # Expected output: [3], [3], [5], [3], [5]
    iter1 = PrimeParameterIterator(num_parameters=1, first_prime=3, max_generated_lists=5)
    print("Actual for num_parameters=1, max_lists=5:")
    for params in iter1:
        print(params)

    print("\nTesting PrimeParameterIterator(num_parameters=2, first_prime=3, max_generated_lists=6)")
    # Expected sequence for num_parameters=2:
    # Base [3] (size 1): Yields [3,3]. Next iter: expand base to [3,5], indices [0,0].
    # Base [3,5] (size 2): Yields [3,3]. Next iter: indices [0,1].
    # Base [3,5] (size 2): Yields [3,5]. Next iter: indices [1,0].
    # Base [3,5] (size 2): Yields [5,3]. Next iter: indices [1,1].
    # Base [3,5] (size 2): Yields [5,5]. Next iter: expand base to [3,5,7], indices [0,0].
    # Base [3,5,7] (size 3): Yields [3,3]. (Stops due to max_generated_lists=6)
    # Expected output: [3,3], [3,3], [3,5], [5,3], [5,5], [3,3]
    iter2 = PrimeParameterIterator(num_parameters=2, first_prime=3, max_generated_lists=6)
    print("Actual for num_parameters=2, max_lists=6:")
    for params in iter2:
        print(params)

    print("\nTesting PrimeParameterIterator(num_parameters=0, first_prime=3, max_generated_lists=2)")
    iter0 = PrimeParameterIterator(num_parameters=0, first_prime=3, max_generated_lists=2)
    print("Actual for num_parameters=0, max_lists=2:")
    # Expected: [], []
    for params in iter0:
        print(params)

    print("\nTesting PrimeParameterIterator(num_parameters=2, first_prime=3, max_generated_lists=0)")
    iter_max_0 = PrimeParameterIterator(num_parameters=2, first_prime=3, max_generated_lists=0)
    print("Actual for num_parameters=2, max_lists=0: (expected no output)")
    for params in iter_max_0:
        print(params)

    print("\nTesting with a slightly larger example to see more of the pattern")
    # num_parameters=2, first_prime=3.
    # Base [3]: [3,3] (1 list)
    # Base [3,5]: [3,3],[3,5],[5,3],[5,5] (4 lists)
    # Base [3,5,7]: [3,3],[3,5],[3,7],[5,3],[5,5],[5,7],[7,3],[7,5],[7,7] (9 lists)
    # Total lists if we go up to base [3,5,7] fully is 1+4+9 = 14.
    # Let's test max_generated_lists = 1 + 4 + 2 = 7 to get part of the third base.
    # Expected: [3,3],  # from base [3]
    #           [3,3], [3,5], [5,3], [5,5], # from base [3,5]
    #           [3,3], [3,5]  # first two from base [3,5,7]
    iter_complex = PrimeParameterIterator(num_parameters=2, first_prime=3, max_generated_lists=7)
    print("Actual for num_parameters=2, max_lists=7:")
    for params in iter_complex:
        print(params)
