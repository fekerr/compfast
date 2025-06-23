# tests/test_celestial_body.py
"""
Unit tests for the CelestialBody class and its related vector math functions.
"""
import unittest
import sys
import os
import math
from collections import deque
import io # For capturing stderr

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from celestial_body import CelestialBody, vec_add, vec_sub, vec_scale, vec_magnitude, vec_normalize

class TestCelestialBody(unittest.TestCase):
    """Test suite for the CelestialBody class."""

    def setUp(self):
        """Common setup for test methods, e.g., creating default body instances."""
        self.default_pos = [0.0, 0.0, 0.0]
        self.default_vel = [0.0, 0.0, 0.0]
        self.body1 = CelestialBody("Body1", 1e24, 6000, "#FFFFFF",
                                   self.default_pos, self.default_vel, max_history=5)
        self.body2 = CelestialBody("Body2", 2e24, 3000, "#FF0000",
                                   [1e9, 0, 0], [0, 1e3, 0], max_history=3)

    def test_initialization(self):
        """Test basic initialization of CelestialBody attributes."""
        self.assertEqual(self.body1.name, "Body1")
        self.assertEqual(self.body1.mass, 1e24)
        self.assertEqual(self.body1.radius, 6000)
        self.assertEqual(self.body1.color, "#FFFFFF")
        self.assertEqual(self.body1.position, self.default_pos)
        self.assertEqual(self.body1.velocity, self.default_vel)
        self.assertEqual(self.body1.acceleration, [0.0, 0.0, 0.0])
        self.assertIsInstance(self.body1.position_history, deque)
        self.assertEqual(self.body1.position_history.maxlen, 5)
        self.assertEqual(len(self.body1.position_history), 1) # Initial position
        self.assertEqual(list(self.body1.position_history[0]), self.default_pos)

    def test_initialization_max_history_edge_cases(self):
        """Test max_history behavior, including zero and negative values."""
        body_zero_hist = CelestialBody("ZeroHist", 1,1,"#000", [0,0,0],[0,0,0], max_history=0)
        self.assertEqual(body_zero_hist.max_history, 0)
        # Deque with maxlen=0 or None behaves differently. We set maxlen=None if max_history=0.
        # If maxlen is None, it's unbounded. If maxlen=0, it's always empty.
        # The code uses
        # So for max_history=0, maxlen will be None (unbounded, but we only append if max_history > 0)
        self.assertEqual(body_zero_hist.position_history.maxlen, None)
        self.assertEqual(len(body_zero_hist.position_history), 0) # No initial pos stored

        with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            body_neg_hist = CelestialBody("NegHist", 1,1,"#000", [0,0,0],[0,0,0], max_history=-5)
            self.assertEqual(body_neg_hist.max_history, 0) # Corrected to 0
            self.assertEqual(body_neg_hist.position_history.maxlen, None)
            self.assertEqual(len(body_neg_hist.position_history), 0)
            self.assertIn("Warning: Invalid max_history '-5'", mock_stderr.getvalue())

        body_one_hist = CelestialBody("OneHist",1,1,"#000",[1,2,3],[0,0,0],max_history=1)
        self.assertEqual(body_one_hist.position_history.maxlen, 1)
        self.assertEqual(len(body_one_hist.position_history), 1)
        body_one_hist.update_post_simulation() # pos is still [1,2,3]
        self.assertEqual(list(body_one_hist.position_history[0]), [1,2,3]) # Still [1,2,3]
        body_one_hist.position = [4,5,6] # Manually change position
        body_one_hist.update_post_simulation()
        self.assertEqual(len(body_one_hist.position_history), 1) # Maxlen is 1
        self.assertEqual(list(body_one_hist.position_history[0]), [4,5,6]) # Now [4,5,6]

    @patch('sys.stderr', new_callable=io.StringIO)
    def test_calculate_gravitational_force(self, mock_stderr):
        """Test gravitational force calculation."""
        # Force of Body2 on Body1
        force_on_1_by_2 = self.body1.calculate_gravitational_force(self.body2)
        # Body1 is at origin, Body2 at [1e9,0,0]. Force on Body1 should be towards Body2 (+x dir)
        self.assertTrue(force_on_1_by_2[0] > 0) # Fx > 0
        self.assertAlmostEqual(force_on_1_by_2[1], 0) # Fy approx 0
        self.assertAlmostEqual(force_on_1_by_2[2], 0) # Fz approx 0

        # Magnitude: G * m1 * m2 / r^2
        G = CelestialBody.GRAVITATIONAL_CONSTANT
        m1 = self.body1.mass; m2 = self.body2.mass
        r_sq = (1e9)**2
        expected_mag = (G * m1 * m2) / r_sq
        self.assertAlmostEqual(vec_magnitude(force_on_1_by_2), expected_mag)

        # Test self-force (should be zero)
        self_force = self.body1.calculate_gravitational_force(self.body1)
        self.assertEqual(self_force, [0.0, 0.0, 0.0])

        # Test zero distance (bodies at same position)
        body3_at_same_pos = CelestialBody("Body3", 1e20, 100, "#00FF00", self.default_pos, self.default_vel)
        zero_dist_force = self.body1.calculate_gravitational_force(body3_at_same_pos)
        self.assertEqual(zero_dist_force, [0.0, 0.0, 0.0])
        self.assertIn("Warning: Zero distance between 'Body1' and 'Body3'", mock_stderr.getvalue())

    def test_get_state_derivatives(self):
        """Test calculation of state derivatives (velocity and acceleration)."""
        temp_pos = [1,2,3]
        temp_vel = [4,5,6]
        net_force = [10,20,30] # Assume mass of body1 is 1.0 for simplicity in this test part
        self.body1.mass = 1.0

        vel_deriv, acc_deriv = self.body1.get_state_derivatives(temp_pos, temp_vel, net_force)
        self.assertEqual(vel_deriv, temp_vel) # dx/dt = v
        self.assertEqual(acc_deriv, [10.0, 20.0, 30.0]) # dv/dt = F/m = F/1.0 = F

        # Test zero mass case
        self.body1.mass = 0.0
        _vel_deriv_zero_mass, acc_deriv_zero_mass = self.body1.get_state_derivatives(temp_pos, temp_vel, net_force)
        self.assertEqual(acc_deriv_zero_mass, [0.0, 0.0, 0.0])

    def test_update_post_simulation(self):
        """Test position history update and maxlen enforcement."""
        self.body1.position_history.clear() # Start with empty history for this test
        self.body1.position_history.append(self.body1.position[:]) # Add initial

        self.assertEqual(len(self.body1.position_history), 1)

        for i in range(10): # Add 10 more positions
            self.body1.position = [i+1, i+1, i+1] # Simulate position change
            self.body1.update_post_simulation()

        self.assertEqual(len(self.body1.position_history), self.body1.max_history) # Should be capped at max_history (5)
        # The last item should be [10,10,10]
        self.assertEqual(list(self.body1.position_history[-1]), [10,10,10])
        # The first item should be [6,6,6] because 0(init),1,2,3,4,5 were pushed out
        self.assertEqual(list(self.body1.position_history[0]), [6,6,6])

        # Test with max_history = 0 (or disabled)
        body_no_hist = CelestialBody("NoHist",1,1,"#000",[0,0,0],[0,0,0],max_history=0)
        body_no_hist.position = [1,1,1]
        body_no_hist.update_post_simulation() # Should not add to history
        self.assertEqual(len(body_no_hist.position_history), 0)


if __name__ == '__main__':
    unittest.main()
