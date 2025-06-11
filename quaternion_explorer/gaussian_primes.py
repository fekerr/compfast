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
        if limit_on_y_squared < 0:
            continue

        max_y = int(math.sqrt(limit_on_y_squared))

        for y in range(max_y + 1):
            if x == 0 and y == 0:
                continue

            if is_gaussian_prime(x, y):
                if x == 0:
                    found_primes_set.add((0, y))
                elif y == 0:
                    found_primes_set.add((x, 0))
                else:
                    found_primes_set.add(tuple(sorted((x, y))))

    return sorted(list(found_primes_set))

if __name__ == '__main__':
    print("is_prime tests:")
    print(f"is_prime(1): {is_prime(1)}")
    print(f"is_prime(2): {is_prime(2)}")
    print(f"is_prime(3): {is_prime(3)}")
    print(f"is_prime(4): {is_prime(4)}")
    print(f"is_prime(19): {is_prime(19)}")
    print(f"is_prime(23): {is_prime(23)}")

    print("\nis_gaussian_prime tests:")
    print(f"is_gaussian_prime(3, 0): {is_gaussian_prime(3, 0)}")
    print(f"is_gaussian_prime(0, 3): {is_gaussian_prime(0, 3)}")
    print(f"is_gaussian_prime(1, 2): {is_gaussian_prime(1, 2)}")
    print(f"is_gaussian_prime(2, 3): {is_gaussian_prime(2, 3)}")
    print(f"is_gaussian_prime(7, 0): {is_gaussian_prime(7, 0)}")
    print(f"is_gaussian_prime(1, 1): {is_gaussian_prime(1, 1)}")
    print(f"is_gaussian_prime(2, 0): {is_gaussian_prime(2, 0)}")
    print(f"is_gaussian_prime(5, 0): {is_gaussian_prime(5, 0)}")
    print(f"is_gaussian_prime(0, 5): {is_gaussian_prime(0, 5)}")
    print(f"is_gaussian_prime(1, 0): {is_gaussian_prime(1, 0)}")
    print(f"is_gaussian_prime(0, 0): {is_gaussian_prime(0, 0)}")
    print(f"is_gaussian_prime(0, 7): {is_gaussian_prime(0, 7)}")
    print(f"is_gaussian_prime(2, 1): {is_gaussian_prime(2, 1)}")
    print(f"is_gaussian_prime(4, 1): {is_gaussian_prime(4, 1)}")
    print(f"is_gaussian_prime(1, 4): {is_gaussian_prime(1, 4)}")
    print(f"is_gaussian_prime(2, 2): {is_gaussian_prime(2, 2)}")

    print("\ngenerate_gaussian_primes tests:")
    print(f"generate_gaussian_primes(10): {generate_gaussian_primes(10)}")
    print(f"generate_gaussian_primes(20): {generate_gaussian_primes(20)}")
    print(f"generate_gaussian_primes(50): {generate_gaussian_primes(50)}")
    print(f"generate_gaussian_primes(1): {generate_gaussian_primes(1)}")
    print(f"generate_gaussian_primes(2): {generate_gaussian_primes(2)}")
    print(f"generate_gaussian_primes(0): {generate_gaussian_primes(0)}")
    print(f"generate_gaussian_primes(-5): {generate_gaussian_primes(-5)}")
    print(f"generate_gaussian_primes(8): {generate_gaussian_primes(8)}")
    print(f"generate_gaussian_primes(3): {generate_gaussian_primes(3)}")
