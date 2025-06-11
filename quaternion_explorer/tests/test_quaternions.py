import unittest
import sys
import os

# Adjust path to import from quaternion_explorer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quaternions import Quaternion

class TestQuaternion(unittest.TestCase):

    # Tests for __init__ and __repr__
    def test_creation_and_representation(self):
        q1 = Quaternion(1, 2, 3, 4)
        self.assertEqual(str(q1), "(1 + 2i + 3j + 4k)")

        q2 = Quaternion(1, -2, 0, -5)
        self.assertEqual(str(q2), "(1 - 2i + 0j - 5k)")

        q3 = Quaternion(0, 0, 0, 0)
        self.assertEqual(str(q3), "(0 + 0i + 0j + 0k)")

        q4 = Quaternion(-1, -2, -3, -4)
        self.assertEqual(str(q4), "(-1 - 2i - 3j - 4k)")

    # Tests for norm_squared()
    def test_norm_squared(self):
        q1 = Quaternion(1, 2, 3, 4)
        self.assertEqual(q1.norm_squared(), 1*1 + 2*2 + 3*3 + 4*4) # 30

        q2 = Quaternion(0, 0, 0, 0)
        self.assertEqual(q2.norm_squared(), 0)

        q3 = Quaternion(1, -1, 1, -1)
        self.assertEqual(q3.norm_squared(), 1*1 + (-1)*(-1) + 1*1 + (-1)*(-1)) # 4

        q4 = Quaternion(5, 0, 0, 0)
        self.assertEqual(q4.norm_squared(), 25)

    # Tests for is_prime()
    def test_is_prime_true_cases(self):
        # Norm squared is prime, and gcd(a,b,c,d) == 1
        self.assertTrue(Quaternion(1, 1, 0, 0).is_prime(), "Q(1,1,0,0) norm_sq=2, gcd=1 -> should be prime")
        self.assertTrue(Quaternion(1, 1, 1, 0).is_prime(), "Q(1,1,1,0) norm_sq=3, gcd=1 -> should be prime")
        self.assertTrue(Quaternion(2, 1, 0, 0).is_prime(), "Q(2,1,0,0) norm_sq=5, gcd=1 -> should be prime")
        self.assertTrue(Quaternion(1, 2, 0, 0).is_prime(), "Q(1,2,0,0) norm_sq=5, gcd=1 -> should be prime")
        self.assertTrue(Quaternion(1, 1, 1, 2).is_prime(), "Q(1,1,1,2) norm_sq=7, gcd=1 -> should be prime")
        self.assertTrue(Quaternion(3, 1, 1, 0).is_prime(), "Q(3,1,1,0) norm_sq=11, gcd=1 -> should be prime") # 9+1+1=11
        # Corrected cases from previous thoughts:
        self.assertTrue(Quaternion(2,1,1,1).is_prime(), "Q(2,1,1,1) norm_sq=7 (prime), gcd=1 -> should be prime")
        self.assertTrue(Quaternion(0,0,1,2).is_prime(), "Q(0,0,1,2) norm_sq=5, gcd=1 -> should be prime")
        self.assertTrue(Quaternion(1,2,1,1).is_prime(), "Q(1,2,1,1) norm_sq=7, gcd=1 -> should be prime")


    def test_is_prime_false_norm_not_prime(self):
        self.assertFalse(Quaternion(1, 0, 0, 0).is_prime(), "Q(1,0,0,0) norm_sq=1 (not prime)")
        self.assertFalse(Quaternion(2, 0, 0, 0).is_prime(), "Q(2,0,0,0) norm_sq=4 (not prime)")
        self.assertFalse(Quaternion(1, 1, 1, 1).is_prime(), "Q(1,1,1,1) norm_sq=4 (not prime)")
        self.assertFalse(Quaternion(2, 2, 0, 0).is_prime(), "Q(2,2,0,0) norm_sq=8 (not prime)") # gcd=2 also
        self.assertFalse(Quaternion(3, 0, 0, 0).is_prime(), "Q(3,0,0,0) norm_sq=9 (not prime)") # gcd=3 also
        self.assertFalse(Quaternion(1, 2, 3, 0).is_prime(), "Q(1,2,3,0) norm_sq=14 (not prime)")
        self.assertFalse(Quaternion(0,1,2,2).is_prime(), "Q(0,1,2,2) norm_sq=9 (not prime)")


    def test_is_prime_false_not_primitive_but_norm_is_prime(self):
        # This case is impossible if norm_squared being prime implies primitivity.
        # Tests where gcd > 1 are covered by norm_not_prime, as g^2 * N(q') = p implies g=1.
        q_non_primitive = Quaternion(2,2,0,0) # norm_sq = 8 (not prime), gcd = 2
        self.assertFalse(q_non_primitive.is_prime())
        q_non_primitive2 = Quaternion(3,3,3,0) # norm_sq = 27 (not prime), gcd = 3
        self.assertFalse(q_non_primitive2.is_prime())
        pass

    def test_zero_quaternion_not_prime(self):
        self.assertFalse(Quaternion(0,0,0,0).is_prime(), "Q(0,0,0,0) should not be prime")


    # Tests for __mul__(self, other)
    def test_multiplication_identity(self):
        q_iden = Quaternion(1, 0, 0, 0)
        q_zero = Quaternion(0, 0, 0, 0)
        q_gen = Quaternion(2, 3, 4, 5)

        self.assertEqual(str(q_iden * q_gen), str(q_gen))
        self.assertEqual(str(q_gen * q_iden), str(q_gen))

        self.assertEqual(str(q_zero * q_gen), str(q_zero))
        self.assertEqual(str(q_gen * q_zero), str(q_zero))

    def test_multiplication_basis_vectors(self):
        q_i = Quaternion(0, 1, 0, 0)
        q_j = Quaternion(0, 0, 1, 0)
        q_k = Quaternion(0, 0, 0, 1)

        # i*j = k
        self.assertEqual(str(q_i * q_j), str(q_k))
        # j*k = i
        self.assertEqual(str(q_j * q_k), str(q_i))
        # k*i = j
        self.assertEqual(str(q_k * q_i), str(q_j))

        # j*i = -k
        self.assertEqual(str(q_j * q_i), str(Quaternion(0, 0, 0, -1)))
        # k*j = -i
        self.assertEqual(str(q_k * q_j), str(Quaternion(0, -1, 0, 0)))
        # i*k = -j
        self.assertEqual(str(q_i * q_k), str(Quaternion(0, 0, -1, 0)))

        # i*i = -1
        self.assertEqual(str(q_i * q_i), str(Quaternion(-1, 0, 0, 0)))
        # j*j = -1
        self.assertEqual(str(q_j * q_j), str(Quaternion(-1, 0, 0, 0)))
        # k*k = -1
        self.assertEqual(str(q_k * q_k), str(Quaternion(-1, 0, 0, 0)))


    def test_multiplication_general(self):
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(5, 6, 7, 8)
        # Expected result from problem description: Q(-60, 12, 30, 24)
        expected_q = Quaternion(-60, 12, 30, 24)
        self.assertEqual(str(q1 * q2), str(expected_q))

        q3 = Quaternion(1,0,0,0) # Identity
        q4 = Quaternion(0,1,2,3)
        self.assertEqual(str(q3*q4), str(q4))

        qa = Quaternion(1,1,0,0) # (1+i)
        qb = Quaternion(1,0,1,0) # (1+j)
        expected_q_ab = Quaternion(1,1,1,1) # (1+i)(1+j) = 1+i+j+k
        self.assertEqual(str(qa*qb), str(expected_q_ab))


if __name__ == '__main__':
    unittest.main()
