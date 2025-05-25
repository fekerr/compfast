import math

def is_prime(n):
    """
    Checks if a number is a prime number.
    n <= 1 are not prime.
    """
    if n <= 1:
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

def is_gaussian_prime(a, b):
    """
    Checks if a + bi is a Gaussian prime.

    A Gaussian integer a + bi is a Gaussian prime if:
    - One of a or b is zero, and the absolute value of the non-zero part is a prime number p
      such that p % 4 == 3.
    - Neither a nor b is zero, and the sum of their squares (a*a + b*b) is a prime number.
    """
    a_abs = abs(a)
    b_abs = abs(b)

    if a == 0 and b == 0:
        return False # 0 is not a Gaussian prime

    if a == 0:
        # Purely imaginary, form is bi (b != 0)
        return is_prime(b_abs) and (b_abs % 4 == 3)
    elif b == 0:
        # Purely real, form is a (a != 0)
        return is_prime(a_abs) and (a_abs % 4 == 3)
    else:
        # Neither a nor b is zero
        norm_sq = a*a + b*b # Norm squared
        return is_prime(norm_sq)

def generate_gaussian_primes(limit_on_norm_squared):
    """
    Generates Gaussian primes a + bi such that their norm squared (a*a + b*b)
    is less than or equal to limit_on_norm_squared.

    Implements the "Final refined logic":
    1. Initialize an empty set found_primes_set.
    2. Iterate x from 0 up to int(sqrt(limit_on_norm_squared)).
    3. Iterate y from 0 up to int(sqrt(limit_on_norm_squared - x*x)).
    4. If x == 0 and y == 0, continue.
    5. If is_gaussian_prime(x, y):
        If x == 0: add (0, y) to found_primes_set.
        Else if y == 0: add (x, 0) to found_primes_set.
        Else (x > 0 and y > 0): add tuple(sorted((x, y))) to found_primes_set.
    6. Convert found_primes_set to a list and sort it before returning.
    """
    if limit_on_norm_squared < 0:
        return []

    found_primes_set = set()
    
    max_x = int(math.sqrt(limit_on_norm_squared))

    for x in range(max_x + 1):
        limit_on_y_squared = limit_on_norm_squared - (x*x)
        # limit_on_y_squared can be negative if x*x itself is slightly larger than limit_on_norm_squared
        # due to floating point issues with sqrt then int().
        # However, max_x should ensure x*x <= limit_on_norm_squared.
        # If limit_on_y_squared is negative, math.sqrt would raise ValueError.
        # So ensure it's not negative before sqrt.
        if limit_on_y_squared < 0:
            continue # Should ideally not be reached if max_x is calculated carefully

        max_y = int(math.sqrt(limit_on_y_squared))
        
        for y in range(max_y + 1):
            if x == 0 and y == 0:
                continue
            
            # By construction of loops, x*x + y*y should be <= limit_on_norm_squared.
            # No need for: norm_sq = x*x + y*y
            # No need for: if norm_sq > limit_on_norm_squared: continue or break

            if is_gaussian_prime(x, y):
                if x == 0: # Form (0, y) where y > 0 (y=0 case is skipped by x=0,y=0 check)
                    found_primes_set.add((0, y))
                elif y == 0: # Form (x, 0) where x > 0 (x=0 case handled above)
                    found_primes_set.add((x, 0))
                else: # x > 0 and y > 0
                    found_primes_set.add(tuple(sorted((x, y))))
    
    return sorted(list(found_primes_set))

if __name__ == '__main__':
    print("is_prime tests:")
    print(f"is_prime(1): {is_prime(1)}") # False
    print(f"is_prime(2): {is_prime(2)}") # True
    print(f"is_prime(3): {is_prime(3)}") # True
    print(f"is_prime(4): {is_prime(4)}") # False
    print(f"is_prime(19): {is_prime(19)}") # True (19%4==3)
    print(f"is_prime(23): {is_prime(23)}") # True (23%4==3)

    print("\nis_gaussian_prime tests:")
    # Examples from prompt
    print(f"is_gaussian_prime(3, 0): {is_gaussian_prime(3, 0)}")   # True
    print(f"is_gaussian_prime(0, 3): {is_gaussian_prime(0, 3)}")   # True
    print(f"is_gaussian_prime(1, 2): {is_gaussian_prime(1, 2)}")   # True
    print(f"is_gaussian_prime(2, 3): {is_gaussian_prime(2, 3)}")   # True
    print(f"is_gaussian_prime(7, 0): {is_gaussian_prime(7, 0)}")   # True
    print(f"is_gaussian_prime(1, 1): {is_gaussian_prime(1, 1)}")   # True
    print(f"is_gaussian_prime(2, 0): {is_gaussian_prime(2, 0)}")   # False
    print(f"is_gaussian_prime(5, 0): {is_gaussian_prime(5, 0)}")   # False
    print(f"is_gaussian_prime(0, 5): {is_gaussian_prime(0, 5)}")   # False
    print(f"is_gaussian_prime(1, 0): {is_gaussian_prime(1, 0)}")   # False
    # Additional tests
    print(f"is_gaussian_prime(0, 0): {is_gaussian_prime(0, 0)}") # False
    print(f"is_gaussian_prime(0, 7): {is_gaussian_prime(0, 7)}") # True
    print(f"is_gaussian_prime(2, 1): {is_gaussian_prime(2, 1)}") # True (associate of 1+2i)
    print(f"is_gaussian_prime(4, 1): {is_gaussian_prime(4, 1)}") # True (16+1=17 prime)
    print(f"is_gaussian_prime(1, 4): {is_gaussian_prime(1, 4)}") # True (1+16=17 prime)
    print(f"is_gaussian_prime(2, 2): {is_gaussian_prime(2, 2)}") # False (4+4=8 not prime)


    print("\ngenerate_gaussian_primes tests:")
    print(f"generate_gaussian_primes(10): {generate_gaussian_primes(10)}")
    # Expected: [(0, 3), (1, 1), (1, 2), (3, 0)] (order may vary before sort)
    # (0,3) norm 9, 3%4=3
    # (1,1) norm 2, prime
    # (1,2) norm 5, prime (2,1) maps to (1,2)
    # (3,0) norm 9, 3%4=3

    print(f"generate_gaussian_primes(20): {generate_gaussian_primes(20)}")
    # Expected: [(0, 3), (1, 1), (1, 2), (1, 4), (2, 3), (3, 0), (4,1)] -> sorted by first element
    # [(0,3), (1,1), (1,2), (1,4), (2,3), (3,0)] - wait, (4,1) stored as (1,4)
    # Should be: [(0, 3), (1, 1), (1, 2), (1, 4), (2, 3), (3, 0)]
    # Let's trace for 20:
    # (0,3) norm 9
    # (1,1) norm 2
    # (1,2) norm 5
    # (1,4) norm 17
    # (2,3) norm 13
    # (3,0) norm 9
    # (0,7) norm 49 > 20. (7%4=3)
    # (3,2) norm 13 -> (2,3)
    # (4,1) norm 17 -> (1,4)
    # My test output for 20 in previous version: [(0,3), (1,1), (1,2), (1,4), (2,3), (3,0)] - this is correct.

    print(f"generate_gaussian_primes(50): {generate_gaussian_primes(50)}")
    # Expected: [(0,3), (0,7), (1,1), (1,2), (1,4), (1,6), (2,3), (2,5), (3,0), (3,4), (4,1)->(1,4), (4,5), (5,2)->(2,5), (5,4)->(4,5), (6,1)->(1,6), (6,5), (7,0)]
    # Sorted: [(0,3), (0,7), (1,1), (1,2), (1,4), (1,6), (2,3), (2,5), (3,0), (3,4), (4,5), (5,6), (6,1) -> (1,6), (6,5), (7,0)]
    # Let's list some:
    # x=0: (0,3) N=9, (0,7) N=49.
    # x=1: (1,1) N=2, (1,2) N=5, (1,4) N=17, (1,6) N=37. (1,0) no (1%4!=3). (1,3) N=10 no. (1,5) N=26 no.
    # x=2: (2,1) -> (1,2). (2,3) N=13. (2,5) N=29. (2,0) no.
    # x=3: (3,0) N=9. (3,2) -> (2,3). (3,4) N=25 no (norm is not prime). Wait, 3*3+4*4=25, 25 is not prime. So (3,4) is not GP.
    #      is_gaussian_prime(3,4) -> is_prime(25) -> False. Correct.
    # x=4: (4,1) -> (1,4). (4,3) -> (3,4) (norm 25, no). (4,5) N=41.
    # x=5: (5,0) no. (5,2) -> (2,5). (5,4) -> (4,5).
    # x=6: (6,1) -> (1,6). (6,5) N=61 (too big, 6*6+5*5=36+25=61. limit_on_norm_squared=50). No (6,5).
    # x=7: (7,0) N=49.
    # So for 50: [(0,3), (0,7), (1,1), (1,2), (1,4), (1,6), (2,3), (2,5), (3,0), (4,1)->(1,4), (4,5), (7,0)]
    # Sorted: [(0, 3), (0, 7), (1, 1), (1, 2), (1, 4), (1, 6), (2, 3), (2, 5), (3, 0), (4, 5), (7, 0)]

    print(f"generate_gaussian_primes(1): {generate_gaussian_primes(1)}") # []
    print(f"generate_gaussian_primes(2): {generate_gaussian_primes(2)}") # [(1,1)]
    print(f"generate_gaussian_primes(0): {generate_gaussian_primes(0)}") # []
    print(f"generate_gaussian_primes(-5): {generate_gaussian_primes(-5)}") # []

    # Test case where x*x could be slightly > limit_on_norm_squared due to float precision
    # e.g. limit = 8, sqrt(8) = 2.828, int(sqrt(8))=2. max_x=2.
    # x=2, x*x=4. limit_on_y_sq = 8-4=4. max_y=int(sqrt(4))=2.
    #   y=0: (2,0) -> GP? no, 2%4!=3.
    #   y=1: (2,1) -> norm 5, GP. Add (1,2).
    #   y=2: (2,2) -> norm 8, not prime. Not GP.
    print(f"generate_gaussian_primes(8): {generate_gaussian_primes(8)}")
    # Expected: [(1,1), (1,2)]
    # (1,1) N=2
    # (2,0) No
    # (0,2) No
    # (1,2) N=5 -> (1,2)
    # (2,1) N=5 -> (1,2)
    # (2,2) N=8 No.
    # (0,1) No.
    # (0,0) skip.
    # For limit 8:
    # x=0: max_y=int(sqrt(8))=2.
    #   y=0: skip
    #   y=1: (0,1) GP? no, 1 not prime.
    #   y=2: (0,2) GP? no, 2%4!=3.
    # x=1: max_y=int(sqrt(8-1))=int(sqrt(7))=2.
    #   y=0: (1,0) GP? no, 1 not prime.
    #   y=1: (1,1) GP? yes, 1*1+1*1=2, prime. Add (1,1).
    #   y=2: (1,2) GP? yes, 1*1+2*2=5, prime. Add (1,2).
    # x=2: max_y=int(sqrt(8-4))=int(sqrt(4))=2.
    #   y=0: (2,0) GP? no, 2%4!=3.
    #   y=1: (2,1) GP? yes, 2*2+1*1=5, prime. Add tuple(sorted(2,1)) -> (1,2).
    #   y=2: (2,2) GP? no, 2*2+2*2=8, not prime.
    # Result: {(1,1), (1,2)} -> sorted [(1,1), (1,2)]. This seems correct.
    # The `if limit_on_y_squared < 0: continue` should handle potential floating point issues robustly.
    # For example if limit_on_norm_squared = 7. max_x = int(sqrt(7)) = 2.
    # x = 2. x*x = 4. limit_on_y_squared = 7 - 4 = 3. max_y = int(sqrt(3)) = 1.
    # y loop up to 1.
    # (2,0) no. (2,1) yes, add (1,2).
    # If limit_on_norm_squared = 3. max_x = int(sqrt(3)) = 1.
    # x=0: max_y=int(sqrt(3))=1. (0,1) no.
    # x=1: max_y=int(sqrt(3-1))=int(sqrt(2))=1. (1,0) no. (1,1) yes, N=2. Add (1,1).
    # Result: [(1,1)]
    # generate_gaussian_primes(3) -> [(1,1)]
    print(f"generate_gaussian_primes(3): {generate_gaussian_primes(3)}")
The file `quaternion_explorer/gaussian_primes.py` has been updated to reflect the "Final refined logic for `generate_gaussian_primes`".
The key changes implemented were:
1.  The outer loop for `x` iterates from `0` to `int(math.sqrt(limit_on_norm_squared))`.
2.  The inner loop for `y` now correctly iterates from `0` to `int(math.sqrt(limit_on_norm_squared - x*x))`.
3.  A check `if limit_on_y_squared < 0: continue` was added before calculating `max_y` to prevent potential `math.sqrt` errors with negative inputs, although this should be rare given `max_x`'s definition.
4.  The redundant check `if norm_sq > limit_on_norm_squared:` was removed as the loop bounds now inherently satisfy this condition.
5.  The logic for adding `(0,y)`, `(x,0)`, or `tuple(sorted((x,y)))` to the `found_primes_set` remains the same, correctly handling uniqueness.
6.  The final result is a sorted list of these unique Gaussian prime tuples.
7.  Docstrings and the `if __name__ == '__main__':` test block are preserved. The tests in the main block were also updated to reflect expected outputs based on the refined logic.

The code now correctly implements the specified algorithm.
