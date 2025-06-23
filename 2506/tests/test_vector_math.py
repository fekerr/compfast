import unittest
import sys
import os
import math # Added for sqrt in test_vec_magnitude

# Add src directory to Python path to import modules from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from celestial_body import vec_add, vec_sub, vec_scale, vec_magnitude, vec_normalize

class TestVectorMath(unittest.TestCase):

    def test_vec_add(self):
        self.assertEqual(vec_add([1, 2, 3], [4, 5, 6]), [5, 7, 9])
        self.assertEqual(vec_add([-1, 0, 1], [1, 0, -1]), [0, 0, 0])
        self.assertEqual(vec_add([0,0,0], [0,0,0]), [0,0,0])

    def test_vec_sub(self):
        self.assertEqual(vec_sub([5, 7, 9], [4, 5, 6]), [1, 2, 3])
        self.assertEqual(vec_sub([0, 0, 0], [1, 2, 3]), [-1, -2, -3])

    def test_vec_scale(self):
        self.assertEqual(vec_scale([1, 2, 3], 2), [2, 4, 6])
        self.assertEqual(vec_scale([1, 2, 3], 0), [0, 0, 0])
        self.assertEqual(vec_scale([-1, -2, -3], -1), [1, 2, 3])

    def test_vec_magnitude(self):
        self.assertAlmostEqual(vec_magnitude([3, 4, 0]), 5.0)
        self.assertAlmostEqual(vec_magnitude([0, 0, 0]), 0.0)
        self.assertAlmostEqual(vec_magnitude([1, 1, 1]), math.sqrt(3)) # Use math.sqrt for precision

    def test_vec_normalize(self):
        self.assertEqual(vec_normalize([0,0,0]), [0,0,0])

        norm_vec1 = vec_normalize([3,4,0])
        self.assertAlmostEqual(vec_magnitude(norm_vec1), 1.0)
        self.assertAlmostEqual(norm_vec1[0], 0.6)
        self.assertAlmostEqual(norm_vec1[1], 0.8)
        self.assertAlmostEqual(norm_vec1[2], 0.0)

        norm_vec2 = vec_normalize([1,1,1])
        self.assertAlmostEqual(vec_magnitude(norm_vec2), 1.0)

if __name__ == '__main__':
    unittest.main()
