import random
from gaussian_primes import generate_gaussian_primes
from quaternions import Quaternion

# Configuration
GAUSSIAN_PRIME_NORM_SQ_LIMIT = 100  # Limit for norm squared of Gaussian primes
NUM_QUATERNIONS_TO_GENERATE = 1000 # Number of quaternions to generate initially

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
    print(f"Generated {len(gaussian_primes_tuples)} Gaussian primes (tuples): {gaussian_primes_tuples}")

    # 2. Create a list of integer components from these Gaussian primes
    print("\nStep 2: Extracting integer components from Gaussian primes")
    integer_components_set = set() 
    for x, y in gaussian_primes_tuples:
        if x != 0:
            integer_components_set.add(x)
        if y != 0:
            integer_components_set.add(y)
            
    if not integer_components_set:
        # This case means that all x and y in all generated Gaussian prime tuples were 0.
        # This should not happen if generate_gaussian_primes works correctly, as (0,0) is not a GP,
        # and other GPs like (1,1) or (0,3) have non-zero components.
        print("Error: No non-zero integer components could be extracted from Gaussian primes. Cannot generate quaternions.")
        return
        
    integer_components_list = sorted(list(integer_components_set)) # Sort for consistent output/testing
    print(f"Extracted {len(integer_components_list)} unique non-zero integer components: {integer_components_list}")

    # 3. Generate Quaternions
    print(f"\nStep 3: Generating {NUM_QUATERNIONS_TO_GENERATE} quaternions")
    generated_quaternions = []
    if not integer_components_list: # Should have been caught above, but as a safeguard
        print("Error: Integer component list is empty. Cannot generate quaternions.")
        return

    for _ in range(NUM_QUATERNIONS_TO_GENERATE):
        # Ensure components can be 0 if 0 is in the list, or only non-zero if specified.
        # The current extraction ensures only non-zero components.
        # If we want 0 as a possible component, it needs to be added to integer_components_list.
        # The prompt says "non-zero components if possible".
        # For now, using only non-zero components extracted.
        a = random.choice(integer_components_list)
        b = random.choice(integer_components_list)
        c = random.choice(integer_components_list)
        d = random.choice(integer_components_list)
        generated_quaternions.append(Quaternion(a, b, c, d))
    
    print(f"Generated {len(generated_quaternions)} quaternions.")
    if generated_quaternions:
        print(f"Example generated quaternion: {generated_quaternions[0]}")


    # 4. Filter for Prime Quaternions
    print("\nStep 4: Filtering for prime quaternions")
    prime_quaternions = []
    for q in generated_quaternions:
        if q.is_prime():
            prime_quaternions.append(q)
    
    print(f"Found {len(prime_quaternions)} prime quaternions out of {len(generated_quaternions)} generated.")
    if prime_quaternions:
        print(f"Example prime quaternion: {prime_quaternions[0]}")


    # 5. Perform Pairwise Quaternion Multiplication
    print("\nStep 5: Performing pairwise quaternion multiplication")
    product_count = 0
    sum_of_product_norms_sq = 0

    if len(prime_quaternions) < 2:
        print("Need at least two prime quaternions to perform pairwise multiplication. Skipping.")
    else:
        for q1 in prime_quaternions:
            for q2 in prime_quaternions:
                # Calculate prod1 = Q1 * Q2
                prod1 = q1 * q2
                product_count += 1
                sum_of_product_norms_sq += prod1.norm_squared()
                
                # Calculate prod2 = Q2 * Q1
                prod2 = q2 * q1
                product_count += 1
                sum_of_product_norms_sq += prod2.norm_squared()
        
        print(f"Total pairwise products calculated: {product_count}")
        print(f"Sum of the squared norms of these product quaternions: {sum_of_product_norms_sq}")
        if product_count > 0:
            average_norm_sq = sum_of_product_norms_sq / product_count
            print(f"Average squared norm of the product quaternions: {average_norm_sq:.2f}")


    print("\nQuaternion operations finished.")

if __name__ == '__main__':
    run_quaternion_operations()
```
