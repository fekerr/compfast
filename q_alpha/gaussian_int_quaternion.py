from q_alpha.integer_gaussian import IntegerGaussian # Use absolute import

# Define symbols for the quaternion basis units for representation purposes
# These are NOT variables storing values, but strings for display
QUAT_I_UNIT_SYMBOL = 'i'
QUAT_J_UNIT_SYMBOL = 'j'
QUAT_K_UNIT_SYMBOL = 'k'
# The scalar unit '1' is implicit

class GaussianIntQuaternion:
    """
    Represents a quaternion with IntegerGaussian coefficients.
    Initialised using 8 integers mapping to the real and imaginary
    parts of the 4 coefficients (w, x, y, z) for 1, i, j, k respectively.
    Q = (p0 + p1*j) + (p2 + p3*j)i + (p4 + p5*j)j + (p6 + p7*j)k
    where j is the complex unit, and i, j, k are quaternion units.
    """
    def __init__(self, p0: int, p1: int, p2: int, p3: int, p4: int, p5: int, p6: int, p7: int):
        params = [p0, p1, p2, p3, p4, p5, p6, p7]
        if not all(isinstance(arg, int) for arg in params):
             raise ValueError("All 8 parameters for GaussianIntQuaternion must be integers.")

        self.w_coeff = IntegerGaussian(p0, p1) # Scalar part
        self.x_coeff = IntegerGaussian(p2, p3) # Coefficient of quaternion unit i
        self.y_coeff = IntegerGaussian(p4, p5) # Coefficient of quaternion unit j
        self.z_coeff = IntegerGaussian(p6, p7) # Coefficient of quaternion unit k

    def __str__(self):
        parts = []
        # Scalar part
        # Only add if it's not zero, or if it's the only part (then 0 should be shown)
        if self.w_coeff != IntegerGaussian(0,0):
             parts.append(f"({str(self.w_coeff)})")

        # Vector parts (i, j, k coefficients)
        coeff_symbol_pairs = [
            (self.x_coeff, QUAT_I_UNIT_SYMBOL),
            (self.y_coeff, QUAT_J_UNIT_SYMBOL),
            (self.z_coeff, QUAT_K_UNIT_SYMBOL)
        ]

        for coeff, symbol in coeff_symbol_pairs:
            if coeff != IntegerGaussian(0,0):
                coeff_str = str(coeff)
                if parts: # If not the first term being added
                    parts.append(f" + ({coeff_str}){symbol}") # Always use " + "
                else: # First term
                    parts.append(f"({coeff_str}){symbol}")


        if not parts: # If w, x, y, z are all zero IntegerGaussians
            return "(0)" # Represent as (0) which implies (0+0j)

        return "".join(parts)


    def __repr__(self):
        return (f"GaussianIntQuaternion(p0={self.w_coeff.real}, p1={self.w_coeff.imag}, "
                f"p2={self.x_coeff.real}, p3={self.x_coeff.imag}, "
                f"p4={self.y_coeff.real}, p5={self.y_coeff.imag}, "
                f"p6={self.z_coeff.real}, p7={self.z_coeff.imag})")

    def __mul__(self, other):
        if not isinstance(other, GaussianIntQuaternion):
            raise TypeError("Can only multiply with another GaussianIntQuaternion.")

        z0, z1, z2, z3 = self.w_coeff, self.x_coeff, self.y_coeff, self.z_coeff
        w0, w1, w2, w3 = other.w_coeff, other.x_coeff, other.y_coeff, other.z_coeff

        # Standard quaternion multiplication rules applied to IntegerGaussian coefficients
        new_w = z0*w0 - z1*w1 - z2*w2 - z3*w3
        new_x = z0*w1 + z1*w0 + z2*w3 - z3*w2
        new_y = z0*w2 - z1*w3 + z2*w0 + z3*w1
        new_z = z0*w3 + z1*w2 - z2*w1 + z3*w0

        return GaussianIntQuaternion(
            new_w.real, new_w.imag,
            new_x.real, new_x.imag,
            new_y.real, new_y.imag,
            new_z.real, new_z.imag
        )

    def conjugate(self):
        # Conjugate of a quaternion q = w + xi + yj + zk is w - xi - yj - zk.
        # The coefficients w,x,y,z are IntegerGaussians here.
        # So we negate the IntegerGaussian coefficients for x, y, z.
        neg_x_coeff = -self.x_coeff
        neg_y_coeff = -self.y_coeff
        neg_z_coeff = -self.z_coeff

        return GaussianIntQuaternion(
            self.w_coeff.real, self.w_coeff.imag, # w_coeff remains unchanged
            neg_x_coeff.real, neg_x_coeff.imag,
            neg_y_coeff.real, neg_y_coeff.imag,
            neg_z_coeff.real, neg_z_coeff.imag
        )

    def __eq__(self, other):
        if not isinstance(other, GaussianIntQuaternion):
            return False
        return (self.w_coeff == other.w_coeff and
                self.x_coeff == other.x_coeff and
                self.y_coeff == other.y_coeff and
                self.z_coeff == other.z_coeff)

# --- Example Usage (Updated) ---
if __name__ == '__main__':
    print("--- IntegerGaussian Examples (from GaussianIntQuaternion context) ---")
    # These examples are primarily for IntegerGaussian but run here for context
    # if this script is executed directly.
    ig1 = IntegerGaussian(1, 2)
    ig2 = IntegerGaussian(3, -4)
    ig_zero = IntegerGaussian(0,0)
    ig_one_real = IntegerGaussian(1,0)
    ig_one_imag = IntegerGaussian(0,1)
    ig_neg_one_imag = IntegerGaussian(0,-1)

    print(f"ig1 = {ig1}")
    print(f"ig2 = {ig2}")
    print(f"str(ig_zero): {str(ig_zero)}")
    print(f"str(ig_one_real): {str(ig_one_real)}")
    print(f"str(ig_one_imag): {str(ig_one_imag)}")
    print(f"str(ig_neg_one_imag): {str(ig_neg_one_imag)}")
    print(f"ig1 + ig2 = {ig1 + ig2}")
    print(f"ig1 * ig2 = {ig1 * ig2}")
    print(f"ig1 == IntegerGaussian(1,2): {ig1 == IntegerGaussian(1,2)}")
    print(f"ig1 == ig2: {ig1 == ig2}")
    print(f"IntegerGaussian(0,0) == IntegerGaussian(0,0): {IntegerGaussian(0,0) == IntegerGaussian(0,0)}")


    print("\n--- GaussianIntQuaternion Examples ---")
    q1 = GaussianIntQuaternion(1, 2, 3, 4, 5, 6, 7, 8)
    print(f"Quaternion q1: {q1}")
    # Expected: (1+2j) + (3+4j)i + (5+6j)j + (7+8j)k (or similar based on __str__ refinements)

    q2 = GaussianIntQuaternion(9, 10, 11, 12, 13, 14, 15, 16)
    print(f"Quaternion q2: {q2}")

    q_zero = GaussianIntQuaternion(0,0,0,0,0,0,0,0)
    print(f"Quaternion q_zero: {q_zero}") # Expected: (0)

    # Example: (1+j) + (2+0j)i = (1+j) + (2)i
    q_simple_real_imag = GaussianIntQuaternion(1,1, 2,0, 0,0, 0,0)
    print(f"Quaternion q_simple_real_imag: {q_simple_real_imag}") # Expected: (1+j) + (2)i

    # Example: (1+j)i
    q_single_coeff = GaussianIntQuaternion(0,0, 1,1, 0,0, 0,0)
    print(f"Quaternion q_single_coeff: {q_single_coeff}") # Expected: (1+j)i

    # Example: (1+j)
    q_scalar_only = GaussianIntQuaternion(1,1, 0,0, 0,0, 0,0)
    print(f"Quaternion q_scalar_only: {q_scalar_only}") # Expected: (1+j)

    q_mixed_zeros = GaussianIntQuaternion(1,1, 0,0, 2,0, 0,-3)
    print(f"Quaternion q_mixed_zeros: {q_mixed_zeros}") # Expected: (1+j) + (2)j + (-3j)k

    q3 = q1 * q2
    print(f"q1 * q2: {q3}")
    # Expected from user's paste: (46-438j) + (-30+57j)i + (-42+76j)j + (-26+118j)k
    # Let's verify for w component:
    # z0*w0 = (1+2j)(9+10j) = 9+10j+18j+20j^2 = 9+28j-20 = -11+28j
    # z1*w1 = (3+4j)(11+12j) = 33+36j+44j+48j^2 = 33+80j-48 = -15+80j
    # z2*w2 = (5+6j)(13+14j) = 65+70j+78j+84j^2 = 65+148j-84 = -19+148j
    # z3*w3 = (7+8j)(15+16j) = 105+112j+120j+128j^2 = 105+232j-128 = -23+232j
    # new_w = (-11+28j) - (-15+80j) - (-19+148j) - (-23+232j)
    #       = -11+28j + 15-80j + 19-148j + 23-232j
    #       = (-11+15+19+23) + (28-80-148-232)j
    #       = (4+19+23) + (-52-148-232)j
    #       = (23+23) + (-200-232)j
    #       = 46 - 432j  -- User's paste had -438j, my calculation is -432j. Will use my calculation.
    # The prompt's example output for q1*q2 might have a slight difference, I will trust the formula.

    q1_conj = q1.conjugate()
    print(f"Conjugate of q1: {q1_conj}")
    # Expected: (1+2j) - (3+4j)i - (5+6j)j - (7+8j)k

    q1_again = GaussianIntQuaternion(1,2,3,4,5,6,7,8)
    print(f"q1 == q1_again: {q1 == q1_again}") # True
    print(f"q1 == q2: {q1 == q2}") # False

    try:
        GaussianIntQuaternion(1, 2.0, 3, 4, 5, 6, 7, 8) # type: ignore
    except ValueError as e:
        print(f"Caught expected error for float input: {e}")

    # This IntegerGaussian test is more appropriate for integer_gaussian.py's main block
    # but is included in the user's paste for GaussianIntQuaternion's main.
    try:
        IntegerGaussian(1, 2.5) # type: ignore
    except TypeError as e:
         print(f"Caught expected error for IntegerGaussian float input: {e}")
