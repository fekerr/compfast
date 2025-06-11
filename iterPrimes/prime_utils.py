import math

def _is_prime(n):
    """Helper function to check if n is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # Iterate from 3 up to sqrt(n) with a step of 2
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def yield_primes(start_prime=2):
    """
    Yields prime numbers indefinitely, starting from start_prime
    or the next prime greater than start_prime.
    """
    num = start_prime
    while True:
        if _is_prime(num):
            yield num
        num += 1 # Check next number

if __name__ == '__main__':
    print("Testing yield_primes(start_prime=3):")
    gen = yield_primes(start_prime=3)
    for _ in range(10):
        print(next(gen)) # Expected: 3, 5, 7, 11, 13, 17, 19, 23, 29, 31

    print("\nTesting yield_primes(start_prime=10):")
    gen2 = yield_primes(start_prime=10)
    for _ in range(5):
        print(next(gen2)) # Expected: 11, 13, 17, 19, 23

    print("\nTesting yield_primes(start_prime=2):")
    gen3 = yield_primes(start_prime=2)
    for _ in range(5):
        print(next(gen3)) # Expected: 2, 3, 5, 7, 11
