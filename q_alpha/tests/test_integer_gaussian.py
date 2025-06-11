import unittest
import sys
import os

from q_alpha.integer_gaussian import IntegerGaussian

class TestIntegerGaussian(unittest.TestCase):
    def test_creation_valid(self):
        g = IntegerGaussian(1, 2)
        self.assertEqual(g.real, 1)
        self.assertEqual(g.imag, 2)
        g_zero = IntegerGaussian(0, 0)
        self.assertEqual(g_zero.real, 0)
        self.assertEqual(g_zero.imag, 0)

    def test_creation_invalid_type(self):
        with self.assertRaisesRegex(TypeError, "Real and imaginary parts of an IntegerGaussian must be integers."):
            IntegerGaussian(1.0, 2)
        with self.assertRaisesRegex(TypeError, "Real and imaginary parts of an IntegerGaussian must be integers."):
            IntegerGaussian(1, 2.5)
        with self.assertRaisesRegex(TypeError, "Real and imaginary parts of an IntegerGaussian must be integers."):
            IntegerGaussian("1", 2)

    def test_addition(self):
        g1 = IntegerGaussian(1, 2)
        g2 = IntegerGaussian(3, -4)
        g_sum = g1 + g2
        self.assertEqual(g_sum.real, 4)
        self.assertEqual(g_sum.imag, -2)
        self.assertIsInstance(g_sum, IntegerGaussian)
        with self.assertRaises(TypeError): # Should be NotImplemented or raise TypeError
            _ = g1 + 3


    def test_subtraction(self):
        g1 = IntegerGaussian(1, 2)
        g2 = IntegerGaussian(3, -4)
        g_diff = g1 - g2
        self.assertEqual(g_diff.real, -2)
        self.assertEqual(g_diff.imag, 6)
        self.assertIsInstance(g_diff, IntegerGaussian)
        with self.assertRaises(TypeError): # Should be NotImplemented or raise TypeError
            _ = g1 - 3

    def test_multiplication_gaussian_by_gaussian(self):
        g1 = IntegerGaussian(1, 2)
        g2 = IntegerGaussian(3, -4)
        # (1+2j)(3-4j) = (1*3 - 2*-4) + (1*-4 + 2*3)j = (3+8) + (-4+6)j = 11+2j
        g_prod = g1 * g2
        self.assertEqual(g_prod.real, 11)
        self.assertEqual(g_prod.imag, 2)
        self.assertIsInstance(g_prod, IntegerGaussian)

    def test_multiplication_gaussian_by_int(self):
        g1 = IntegerGaussian(1, 2)
        scalar = 3
        g_prod_scalar_right = g1 * scalar
        self.assertEqual(g_prod_scalar_right.real, 3)
        self.assertEqual(g_prod_scalar_right.imag, 6)
        self.assertIsInstance(g_prod_scalar_right, IntegerGaussian)

        g_prod_scalar_left = scalar * g1
        self.assertEqual(g_prod_scalar_left.real, 3)
        self.assertEqual(g_prod_scalar_left.imag, 6)
        self.assertIsInstance(g_prod_scalar_left, IntegerGaussian)

        with self.assertRaises(TypeError): # Should be NotImplemented or raise TypeError
            _ = g1 * "str"


    def test_negation(self):
        g1 = IntegerGaussian(1, -2)
        g_neg = -g1
        self.assertEqual(g_neg.real, -1)
        self.assertEqual(g_neg.imag, 2)
        self.assertIsInstance(g_neg, IntegerGaussian)

    def test_equality(self):
        g1 = IntegerGaussian(1, 2)
        g2 = IntegerGaussian(1, 2)
        g3 = IntegerGaussian(1, 3)
        g4 = IntegerGaussian(3, 2)
        self.assertEqual(g1, g2)
        self.assertTrue(g1 == g2)
        self.assertNotEqual(g1, g3)
        self.assertTrue(g1 != g3)
        self.assertNotEqual(g1, g4)
        self.assertFalse(g1 == "1+2j") # Test against different type

    def test_string_representation(self):
        self.assertEqual(str(IntegerGaussian(1, 2)), "1+2j")
        self.assertEqual(str(IntegerGaussian(1, -2)), "1-2j")
        self.assertEqual(str(IntegerGaussian(0, 2)), "2j")
        self.assertEqual(str(IntegerGaussian(0, -2)), "-2j")
        self.assertEqual(str(IntegerGaussian(1, 0)), "1")
        self.assertEqual(str(IntegerGaussian(0, 0)), "0")
        self.assertEqual(str(IntegerGaussian(1, 1)), "1+j")
        self.assertEqual(str(IntegerGaussian(1, -1)), "1-j")
        self.assertEqual(str(IntegerGaussian(0, 1)), "j")
        self.assertEqual(str(IntegerGaussian(0, -1)), "-j")
        self.assertEqual(str(IntegerGaussian(-1, -1)), "-1-j")
        self.assertEqual(str(IntegerGaussian(-1, 1)), "-1+j")


    def test_repr_representation(self):
        g = IntegerGaussian(1, 2)
        self.assertEqual(repr(g), "IntegerGaussian(1, 2)")
        g_neg = IntegerGaussian(-1, -5)
        self.assertEqual(repr(g_neg), "IntegerGaussian(-1, -5)")

if __name__ == '__main__':
    unittest.main()
