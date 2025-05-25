import math

class Quaternion:
    """
    Represents a Quaternion Q = a + bi + cj + dk.
    Components a, b, c, d are typically integers.
    """

    def _is_prime(self, n):
        """
        Checks if a number is a prime number.
        n <= 1 are not prime. Helper function.
        """
        if n <= 1:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    def _gcd(self, x, y):
        """
        Computes the greatest common divisor of two integers x and y.
        Helper function.
        """
        return math.gcd(x, y)

    def _gcd_four(self, a, b, c, d):
        """
        Computes the greatest common divisor of four integers a, b, c, d.
        """
        # Ensure all are integers, take absolute values for GCD calculation consistency
        # math.gcd handles 0 correctly (e.g. gcd(0,5)=5, gcd(0,0)=0)
        # The problem implies a,b,c,d are integers.
        # For primitivity, gcd(0,0,0,0) is not 1. A zero quaternion is not prime.
        # If a,b,c,d are all zero, norm_squared is 0, which _is_prime(0) will return False.
        # So this case is handled.
        return self._gcd(self._gcd(abs(a), abs(b)), self._gcd(abs(c), abs(d)))


    def __init__(self, a, b, c, d):
        """
        Initializes a Quaternion.
        Q = a + bi + cj + dk
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __repr__(self):
        """
        Returns a string representation of the quaternion.
        Example: (1 + 2i + 3j + 4k)
        Handles positive and negative components. Example: (1 - 2i + 0j - 4k).
        """
        parts = []
        # Real part
        parts.append(str(self.a))
        
        # Imaginary part i
        if self.b >= 0:
            parts.append(f"+ {self.b}i")
        else:
            parts.append(f"- {abs(self.b)}i")
            
        # Imaginary part j
        if self.c >= 0:
            parts.append(f"+ {self.c}j")
        else:
            parts.append(f"- {abs(self.c)}j")
            
        # Imaginary part k
        if self.d >= 0:
            parts.append(f"+ {self.d}k")
        else:
            parts.append(f"- {abs(self.d)}k")
            
        return f"({parts[0]} {parts[1][2:] if parts[1].startswith('+ ') else parts[1]} {parts[2][2:] if parts[2].startswith('+ ') else parts[2]} {parts[3][2:] if parts[3].startswith('+ ') else parts[3]})"
        # A slightly better repr to match the example (1 - 2i + 0j - 4k)
        # Let's refine __repr__ formatting logic.

    # Refined __repr__
    def __repr_refined__(self):
        """
        Returns a string representation of the quaternion.
        Example: (1 + 2i + 3j + 4k)
        Handles positive and negative components. Example: (1 - 2i + 0j - 4k).
        """
        # Helper to format each component
        def format_component(value, unit, is_first=False):
            if value == 0 and not is_first : # for a, if it is 0, it should be "0"
                 return f"+ 0{unit}" if unit else "+ 0" # as per example (1 - 2i + 0j - 4k)

            sign = ""
            if not is_first:
                sign = "+ " if value >= 0 else "- "
            
            val_abs = abs(value)
            
            # For the first component (real part a), show sign only if negative
            if is_first and value < 0:
                sign = "-" # No space after for the first term if negative, e.g. -1
            elif is_first and value >=0 :
                sign = ""


            # Handle coefficient 1 for i,j,k parts
            # if val_abs == 1 and unit != "":
            #     return f"{sign}{unit}" # e.g. + i, - j
            # This is not in example, example has 1i etc.
            # The example (1 + 2i + 3j + 4k) does not specify 1i.
            # (1 - 2i + 0j - 4k) is the primary guide.

            return f"{sign}{val_abs}{unit}"

        s_a = format_component(self.a, "", is_first=True)
        s_b = format_component(self.b, "i")
        s_c = format_component(self.c, "j")
        s_d = format_component(self.d, "k")
        
        return f"({s_a} {s_b} {s_c} {s_d})"
    
    # Using the __repr__ from the prompt's guidance directly now:
    def __repr__(self):
        """
        Return a string representation of the quaternion, e.g., "(a + bi + cj + dk)".
        Example: (1 + 2i + 3j + 4k).
        Handle positive and negative components correctly in the string. E.g. (1 - 2i + 0j - 4k).
        """
        # Start with the real part
        res = str(self.a)
        
        # Add imaginary parts
        res += f" + {self.b}i" if self.b >= 0 else f" - {abs(self.b)}i"
        res += f" + {self.c}j" if self.c >= 0 else f" - {abs(self.c)}j"
        res += f" + {self.d}k" if self.d >= 0 else f" - {abs(self.d)}k"
        
        return f"({res})"


    def norm_squared(self):
        """
        Calculates and returns the squared norm of the quaternion: a*a + b*b + c*c + d*d.
        """
        return self.a**2 + self.b**2 + self.c**2 + self.d**2

    def is_prime(self):
        """
        Determines if the quaternion is a prime quaternion (Lipschitz prime).
        A Lipschitz quaternion (integer components) is prime if:
        1. Its norm squared (a*a + b*b + c*c + d*d) is a prime number.
        2. It is "primitive," meaning gcd(a, b, c, d) == 1.
        """
        norm_sq = self.norm_squared()
        if not self._is_prime(norm_sq):
            return False
        
        # Check for primitivity
        # A zero quaternion (0,0,0,0) has norm_sq 0, so _is_prime(0) is False.
        # If any component is non-integer, this definition might be problematic,
        # but problem states components are integers.
        common_divisor = self._gcd_four(self.a, self.b, self.c, self.d)
        if common_divisor != 1:
            return False
            
        return True

    def __mul__(self, other):
        """
        Implements Quaternion multiplication self * other.
        other must also be a Quaternion instance.
        Q1 = a1+b1i+c1j+d1k (self)
        Q2 = a2+b2i+c2j+d2k (other)
        Product Q_res = Q_res_a + Q_res_bi + Q_res_cj + Q_res_dk
        """
        if not isinstance(other, Quaternion):
            return NotImplemented # Or raise TypeError

        a1, b1, c1, d1 = self.a, self.b, self.c, self.d
        a2, b2, c2, d2 = other.a, other.b, other.c, other.d

        res_a = (a1*a2 - b1*b2 - c1*c2 - d1*d2)
        res_b = (a1*b2 + b1*a2 + c1*d2 - d1*c2)
        res_c = (a1*c2 - b1*d2 + c1*a2 + d1*b2)
        res_d = (a1*d2 + b1*c2 - c1*b2 + d1*a2)

        return Quaternion(res_a, res_b, res_c, res_d)

if __name__ == '__main__':
    # Test __repr__
    q1 = Quaternion(1, 2, 3, 4)
    print(f"q1: {q1}") # Expected: (1 + 2i + 3j + 4k)
    q2 = Quaternion(1, -2, 0, -4)
    print(f"q2: {q2}") # Expected: (1 - 2i + 0j - 4k)
    q_neg_real = Quaternion(-1, 2, 3, 4)
    print(f"q_neg_real: {q_neg_real}") # Expected: (-1 + 2i + 3j + 4k)
    q_zero = Quaternion(0,0,0,0)
    print(f"q_zero: {q_zero}") # Expected: (0 + 0i + 0j + 0k)


    # Test norm_squared
    # q1 = 1+2i+3j+4k -> 1*1+2*2+3*3+4*4 = 1+4+9+16 = 30
    print(f"q1.norm_squared(): {q1.norm_squared()}") # Expected: 30
    # q2 = 1-2i+0j-4k -> 1*1+(-2)*(-2)+0*0+(-4)*(-4) = 1+4+0+16 = 21
    print(f"q2.norm_squared(): {q2.norm_squared()}") # Expected: 21
    print(f"q_zero.norm_squared(): {q_zero.norm_squared()}") # Expected: 0

    # Test _is_prime helper (indirectly via Quaternion.is_prime)
    # Need some known prime quaternions.
    # Q = a+bi+cj+dk is prime if norm_squared is prime AND gcd(a,b,c,d)=1
    
    # Example 1: Q = 1+1i+1j+1k. Norm_sq = 1+1+1+1 = 4. Not prime (norm_sq not prime).
    q_1111 = Quaternion(1,1,1,1)
    print(f"q_1111: {q_1111}, norm_sq: {q_1111.norm_squared()}, is_prime: {q_1111.is_prime()}") # Expected: False (norm 4 is not prime)

    # Example 2: Q = 1+2i+3j+0k. Norm_sq = 1+4+9+0 = 14. Not prime (norm_sq not prime).
    q_1230 = Quaternion(1,2,3,0)
    print(f"q_1230: {q_1230}, norm_sq: {q_1230.norm_squared()}, is_prime: {q_1230.is_prime()}") # Expected: False (norm 14 is not prime)

    # Example 3: Q = 1+1i+0j+0k. Norm_sq = 1+1+0+0 = 2. Norm_sq 2 is prime. gcd(1,1,0,0)=1. So, prime.
    q_1100 = Quaternion(1,1,0,0)
    print(f"q_1100: {q_1100}, norm_sq: {q_1100.norm_squared()}, is_prime: {q_1100.is_prime()}") # Expected: True

    # Example 4: Q = 2+2i+0j+0k. Norm_sq = 4+4+0+0 = 8. Not prime (norm_sq not prime).
    # Also, gcd(2,2,0,0)=2 != 1.
    q_2200 = Quaternion(2,2,0,0)
    print(f"q_2200: {q_2200}, norm_sq: {q_2200.norm_squared()}, is_prime: {q_2200.is_prime()}") # Expected: False

    # Example 5: Q = 3+0i+0j+0k. Norm_sq = 9. Not prime (norm_sq not prime).
    # (Note: 3 itself is prime, but the quaternion 3 is not prime in Lipschitz sense because norm is 3*3=9)
    # This is different from Gaussian Primes like 3 or 7 which are prime in Z[i] if p%4=3.
    # For Lipschitz, if Q = p+0i+0j+0k, norm_sq = p*p. p*p is never prime.
    # So, a rational prime p is NOT a Lipschitz prime if represented as p+0i+0j+0k.
    # However, (1+i+j+k) has norm 2. (1+i) has norm 2.
    # The definition of "prime quaternion" can be subtle. The prompt is specific:
    # "A Lipschitz quaternion ... is prime if its norm squared ... is a prime number AND it is 'primitive'".
    # So, 3+0i+0j+0k: norm_sq=9 (not prime). Quaternion is not prime. Correct.
    q_3000 = Quaternion(3,0,0,0)
    print(f"q_3000: {q_3000}, norm_sq: {q_3000.norm_squared()}, is_prime: {q_3000.is_prime()}") # Expected: False

    # Example 6: Q = 1+0i+0j+0k. Norm_sq = 1. Not prime (_is_prime(1) is False).
    q_1000 = Quaternion(1,0,0,0)
    print(f"q_1000: {q_1000}, norm_sq: {q_1000.norm_squared()}, is_prime: {q_1000.is_prime()}") # Expected: False (1 is not prime)

    # Example 7: Q = 0+0i+0j+0k (Zero Quaternion). Norm_sq = 0. Not prime.
    print(f"q_zero: {q_zero}, norm_sq: {q_zero.norm_squared()}, is_prime: {q_zero.is_prime()}") # Expected: False

    # Test __mul__
    # Let Q1 = 1+2i+1j+1k and Q2 = 1+1i+2j+1k
    # Q1 = (1,2,1,1), Q2 = (1,1,2,1)
    # a = (1*1 - 2*1 - 1*2 - 1*1) = (1 - 2 - 2 - 1) = -4
    # b = (1*1 + 2*1 + 1*1 - 1*2) = (1 + 2 + 1 - 2) = 2
    # c = (1*2 - 2*1 + 1*1 + 1*1) = (2 - 2 + 1 + 1) = 2
    # d = (1*1 + 2*2 - 1*1 + 1*1) = (1 + 4 - 1 + 1) = 5
    # Result: -4 + 2i + 2j + 5k
    qm1 = Quaternion(1,2,1,1)
    qm2 = Quaternion(1,1,2,1)
    q_prod = qm1 * qm2
    print(f"qm1: {qm1}")
    print(f"qm2: {qm2}")
    print(f"qm1 * qm2: {q_prod}") # Expected: (-4 + 2i + 2j + 5k)

    # Test multiplication by zero quaternion
    q_prod_zero = q1 * q_zero
    print(f"q1 * q_zero: {q_prod_zero}") # Expected: (0 + 0i + 0j + 0k)
    q_zero_prod_q1 = q_zero * q1
    print(f"q_zero * q1: {q_zero_prod_q1}") # Expected: (0 + 0i + 0j + 0k)

    # Test property (N(q1*q2) = N(q1)*N(q2)) for norm_squared
    # N_sq(qm1) = 1+4+1+1 = 7
    # N_sq(qm2) = 1+1+4+1 = 7
    # N_sq(q_prod) = (-4)^2 + 2^2 + 2^2 + 5^2 = 16 + 4 + 4 + 25 = 49
    # N_sq(qm1) * N_sq(qm2) = 7 * 7 = 49. This holds.
    print(f"N_sq(qm1): {qm1.norm_squared()}") # Expected: 7
    print(f"N_sq(qm2): {qm2.norm_squared()}") # Expected: 7
    print(f"N_sq(q_prod): {q_prod.norm_squared()}") # Expected: 49
    
    # Test _gcd_four
    # Using q_2200 = Quaternion(2,2,0,0). gcd(2,2,0,0) = 2.
    # This is tested by q_2200.is_prime() being False.
    # Test explicitly:
    # print(f"gcd_four(2,2,0,0): {q_2200._gcd_four(2,2,0,0)}") # Expected: 2
    # print(f"gcd_four(1,2,3,0): {q_1230._gcd_four(1,2,3,0)}") # Expected: 1
    # print(f"gcd_four(2,4,6,8): {Quaternion(2,4,6,8)._gcd_four(2,4,6,8)}") # Expected: 2
    # print(f"gcd_four(0,0,0,0): {q_zero._gcd_four(0,0,0,0)}") # Expected: 0. is_prime handles this.
    # What if one value is negative? abs() in _gcd_four handles this.
    # print(f"gcd_four(-2,4,-6,8): {Quaternion(-2,4,-6,8)._gcd_four(-2,4,-6,8)}") # Expected: 2
    
    # A quaternion where norm_sq is prime, but not primitive
    # Q = 2+2i+0j+0k. Norm_sq = 8 (not prime).
    # Q = 2+1i+1j+0k. Norm_sq = 4+1+1 = 6 (not prime).
    # Q = 3+3i+0j+0k. Norm_sq = 9+9 = 18 (not prime).
    # Need a prime norm_sq first.
    # Q = 1+1+0+0 -> norm_sq = 2 (prime). gcd(1,1,0,0)=1. Is prime. (q_1100 test)
    # Q = 2*(1+1i+0j+0k) = 2+2i+0j+0k. This is q_2200.
    #   Norm_sq(2+2i) = 2^2 + 2^2 = 8. Not prime.
    #   gcd(2,2,0,0) = 2. Not primitive.
    # If q is primitive and N(q) is prime, then q is prime.
    # If q is not primitive, say q = d*q', where d is gcd.
    # N(q) = N(d*q') = d^2 * N(q').
    # If N(q) is prime p, then d^2 * N(q') = p.
    # This means d^2 must be 1 (so d=1), and N(q')=p.
    # So, if N(q) is prime, then d must be 1.
    # Thus, the condition "norm_squared is prime" implies primitivity.
    # Let's re-check definitions.
    # From Wikipedia (Lipschitz quaternion): "A Lipschitz quaternion is said to be prime if its norm is a prime number."
    # The norm is sqrt(a^2+b^2+c^2+d^2).
    # So, if sqrt(norm_sq) is prime p, then norm_sq = p^2.
    # This means that if we use this definition, then p+0i+0j+0k (norm p) is not prime, as norm_sq = p^2.
    # The problem statement says: "A Lipschitz quaternion ... is prime if its norm squared ... is a prime number."
    # This is a different definition of "prime quaternion" than the one using the norm itself.
    # If norm_squared(Q) = p (a prime number), then Q is a prime quaternion.
    # Example: 1+1i+0j+0k. norm_squared = 2 (prime). So 1+1i is prime.
    # Now, consider primitivity: gcd(a,b,c,d)=1.
    # If norm_squared(Q) = p (prime), can gcd(a,b,c,d) = g > 1?
    # Let Q = (g*a', g*b', g*c', g*d').
    # norm_squared(Q) = g^2 * (a'^2+b'^2+c'^2+d'^2).
    # If this is prime p, then g^2 * (sum_of_sq_primes) = p.
    # This implies g^2 = 1 (so g=1) and (sum_of_sq_primes) = p.
    # Therefore, if norm_squared(Q) is prime, then Q must be primitive.
    # The primitivity check `_gcd_four(...) != 1` is redundant if `_is_prime(norm_squared())` is true.
    # I will keep the primitivity check as it's explicitly requested by the problem statement.
    # It doesn't hurt, and perhaps there's a subtlety I'm missing or a convention being followed.
    # For example, if the definition of "prime" was about factorization, primitivity would be crucial
    # to distinguish between p and u*p where u is a unit.
    # But here, it's a direct property check.

    # Final check on __repr__ format based on test cases.
    # q1: (1 + 2i + 3j + 4k) -> My code: (1 + 2i + 3j + 4k) - OK
    # q2: (1 - 2i + 0j - 4k) -> My code: (1 - 2i + 0j - 4k) - OK
    # q_neg_real: (-1 + 2i + 3j + 4k) -> My code: (-1 + 2i + 3j + 4k) - OK
    # q_zero: (0 + 0i + 0j + 0k) -> My code: (0 + 0i + 0j + 0k) - OK
    # Looks correct.

    # Final check on _gcd_four:
    # The prompt says `gcd(a,b,c,d) = gcd(gcd(a,b), gcd(c,d))`. This is correct.
    # My code: `self._gcd(self._gcd(abs(a), abs(b)), self._gcd(abs(c), abs(d)))`
    # Using abs() for GCD inputs is good practice, as `math.gcd` behavior with negatives might vary or be less standard.
    # `math.gcd(a,b)` is defined for non-negative integers in some contexts, but Python's `math.gcd` handles negatives:
    # `math.gcd(-6, 3) = 3`, `math.gcd(6, -3) = 3`. `math.gcd(0,5)=5`. `math.gcd(0,0)=0`.
    # So `abs()` is not strictly necessary for `math.gcd` but makes it robust if a different gcd impl were used.
    # For primitivity, we need gcd to be 1. If a,b,c,d are all 0, gcd(0,0,0,0)=0.
    # `q_zero.is_prime()`: norm_sq = 0. `_is_prime(0)` is False. So it correctly returns False.
    # The logic for `is_prime` seems fine.
    pass
