import random
from gaussian_primes import generate_gaussian_primes
from quaternions import Quaternion

# Configuration
GAUSSIAN_PRIME_NORM_SQ_LIMIT = 300  # Limit for norm squared of Gaussian primes
NUM_QUATERNIONS_TO_GENERATE = 100000 # Number of quaternions to generate initially

def run_quaternion_operations():
    """
    Main function to run the quaternion generation and multiplication process.
    """
    print("Starting quaternion operations...")

    # 1. Generate Gaussian Primes
    print(f"\nStep 1: Generating Gaussian primes with norm_sq limit = {GAUSSIAN_PRIME_NORM_SQ_LIMIT}")
    gaussian_primes_tuples = generate_gaussian_primes(GAUSSIAN_PRIME_NORM_SQ_LIMIT)

    if not gaussian_primes_tuples:
        print("Error: No Gaussian primes generated. Try increasing GAUSSIAN_PRIME_NORM_SQ_LIMIT or check gaussian_primes.py.")
        return
    print(f"Generated {len(gaussian_primes_tuples)} Gaussian primes (tuples).") # Truncated for brevity in log
    if len(gaussian_primes_tuples) < 20: # Print all if list is short
         print(f"Generated tuples: {gaussian_primes_tuples}")


    # 2. Create a list of integer components from these Gaussian primes
    print("\nStep 2: Extracting integer components from Gaussian primes")
    integer_components_set = set()
    for x, y in gaussian_primes_tuples:
        if x != 0:
            integer_components_set.add(x)
        if y != 0: # Allow y if x is 0
            integer_components_set.add(y)

    if not integer_components_set:
        print("Error: No non-zero integer components could be extracted from Gaussian primes. Cannot generate quaternions.")
        return

    integer_components_list = sorted(list(integer_components_set))
    print(f"Extracted {len(integer_components_list)} unique integer components.")
    if len(integer_components_list) < 20: # Print all if list is short
        print(f"Components: {integer_components_list}")


    # 3. Generate Quaternions
    print(f"\nStep 3: Generating {NUM_QUATERNIONS_TO_GENERATE} quaternions")
    generated_quaternions = []
    if not integer_components_list:
        print("Error: Integer component list is empty. Cannot generate quaternions.")
        return

    for _ in range(NUM_QUATERNIONS_TO_GENERATE):
        a = random.choice(integer_components_list)
        b = random.choice(integer_components_list)
        c = random.choice(integer_components_list)
        d = random.choice(integer_components_list)
        generated_quaternions.append(Quaternion(a, b, c, d))

    print(f"Generated {len(generated_quaternions)} quaternions.")
    if generated_quaternions and len(generated_quaternions) > 0 : # Check if list is not empty
        print(f"Example generated quaternion: {generated_quaternions[0]}")


    # 4. Filter for Prime Quaternions
    print("\nStep 4: Filtering for prime quaternions")
    prime_quaternions = []
    if not generated_quaternions: # Check if list is not empty
        print("No quaternions were generated to filter.")
    else:
        for q_idx, q in enumerate(generated_quaternions):
            if q.is_prime():
                prime_quaternions.append(q)
            if (q_idx + 1) % 10000 == 0: # Progress update
                print(f"  ...filtered {q_idx+1}/{len(generated_quaternions)} quaternions...")

    print(f"Found {len(prime_quaternions)} prime quaternions out of {len(generated_quaternions)} generated.")
    if prime_quaternions and len(prime_quaternions) > 0: # Check if list is not empty
        print(f"Example prime quaternion: {prime_quaternions[0]}")


    # 5. Perform Pairwise Quaternion Multiplication
    print("\nStep 5: Performing pairwise quaternion multiplication")
    product_count = 0
    sum_of_product_norms_sq = 0

    if len(prime_quaternions) < 1: # Changed from < 2 to < 1 as even 1 prime quaternion means no pairs.
         print("Need at least one prime quaternion to find pairs. If only one, no pairs will be formed. Skipping multiplication if less than 1.")
    elif len(prime_quaternions) < 2:
         print("Only one prime quaternion found. No pairs to multiply. Skipping multiplication.")
    else:
        num_prime_q = len(prime_quaternions)
        total_mult_ops = num_prime_q * num_prime_q * 2 # For Q1*Q2 and Q2*Q1
        print(f"  Starting multiplication for {num_prime_q} prime quaternions (approx {total_mult_ops} operations)...")
        processed_pairs = 0
        for i, q1 in enumerate(prime_quaternions):
            for q2 in prime_quaternions:
                prod1 = q1 * q2
                product_count += 1
                sum_of_product_norms_sq += prod1.norm_squared()

                prod2 = q2 * q1 # q2 * q1
                product_count += 1
                sum_of_product_norms_sq += prod2.norm_squared()
                processed_pairs +=1 # counts one pair (q1,q2) yielding two products
            if (i + 1) % (num_prime_q // 10 if num_prime_q > 10 else 1) == 0 : # Progress update
                print(f"    ...multiplied {i+1}/{num_prime_q} prime quaternions (processed {processed_pairs} pairs)...")

        print(f"Total pairwise products calculated: {product_count}")
        print(f"Sum of the squared norms of these product quaternions: {sum_of_product_norms_sq}")
        if product_count > 0:
            average_norm_sq = sum_of_product_norms_sq / product_count
            print(f"Average squared norm of the product quaternions: {average_norm_sq:.2f}")

    print("\nQuaternion operations finished.")

if __name__ == '__main__':
    run_quaternion_operations()
```
