# iterPrimes: Prime Parameter Iterator

This directory contains tools for generating sequences of prime number parameters.

## Files

-   `prime_utils.py`: Contains a utility function `yield_primes(start_prime)` that generates prime numbers indefinitely, starting from `start_prime` (or the next prime greater than `start_prime` if `start_prime` itself is not prime).
-   `prime_parameter_iterator.py`: Contains the `PrimeParameterIterator` class.

## `PrimeParameterIterator`

The `PrimeParameterIterator` class generates lists of integers, where each list contains `num_parameters` prime numbers. The iteration proceeds by exhausting all combinations for a growing set of available primes.

### How it Works

For a given `num_parameters` (e.g., 2) and `first_prime` (e.g., 3):

1.  **Round 1**: The smallest prime (`3`) forms the initial set of available primes: `P = [3]`.
    The iterator yields all combinations of `num_parameters` length using primes from `P`.
    For `num_parameters=2`, this is `[3,3]`.
2.  **Round 2**: The next prime (`5`) is added to the set: `P = [3,5]`.
    The iterator yields all combinations using this new set `P`.
    For `num_parameters=2`, these are `[3,3], [3,5], [5,3], [5,5]`.
3.  **Round 3**: The next prime (`7`) is added: `P = [3,5,7]`.
    The iterator yields all combinations from this set `P`.
    For `num_parameters=2`, these are `[3,3], [3,5], [3,7], [5,3], [5,5], [5,7], [7,3], [7,5], [7,7]`.
4.  This process continues, adding one new prime to the set for each "round" of combination generation.

The iterator yields these lists sequentially across rounds. So, the actual output for `num_parameters=2, first_prime=3` would be:
`[3,3]` (from round 1)
`[3,3], [3,5], [5,3], [5,5]` (from round 2)
`[3,3], [3,5], [3,7], [5,3], [5,5], [5,7], [7,3], [7,5], [7,7]` (from round 3)
...and so on.

### Usage Example

```python
from iterPrimes.prime_parameter_iterator import PrimeParameterIterator

# Create an iterator for 2 parameters, starting with prime 3, limit to 7 lists
iterator = PrimeParameterIterator(num_parameters=2, first_prime=3, max_generated_lists=7)

print("Generating parameter lists:")
for param_list in iterator:
    print(param_list)

# Expected Output:
# Generating parameter lists:
# [3, 3]
# [3, 3]
# [3, 5]
# [5, 3]
# [5, 5]
# [3, 3]
# [3, 5]
```

The `if __name__ == '__main__':` block in `prime_parameter_iterator.py` contains more examples demonstrating its behavior.
