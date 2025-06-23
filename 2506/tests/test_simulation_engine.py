# tests/test_simulation_engine.py
"""
Unit tests for the SimulationEngine class.
Focuses on initialization and core force calculation logic.
"""
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from simulation_engine import SimulationEngine
# Mock CelestialBody for these tests to isolate SimulationEngine logic
from celestial_body import CelestialBody # Import for type hinting, but will be mocked

class TestSimulationEngine(unittest.TestCase):
    """Test suite for SimulationEngine."""

    def test_initialization(self):
        """Test engine initialization with bodies and time step."""
        mock_body1 = MagicMock(spec=CelestialBody)
        mock_body2 = MagicMock(spec=CelestialBody)
        bodies = [mock_body1, mock_body2]
        base_time_step = 0.1

        engine = SimulationEngine(bodies, base_time_step, integration_method='rk4')

        self.assertEqual(list(engine.bodies), bodies) # Ensure it's a copy if list() was used
        self.assertEqual(engine.base_time_step, base_time_step)
        self.assertEqual(engine.integration_method, 'rk4')

    def test_initialization_empty_bodies_warning(self):
        """Test warning when initialized with no bodies."""
        with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            engine = SimulationEngine([], 0.1)
            self.assertIn("Warning: SimulationEngine initialized with no celestial bodies.", mock_stderr.getvalue())

    def test_initialization_unknown_method_warning(self):
        """Test warning for unknown integration method and fallback to rk4."""
        with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            engine = SimulationEngine([], 0.1, integration_method='unknown_method')
            self.assertIn("Warning: Unknown integration method 'unknown_method'. Defaulting to 'rk4'.", mock_stderr.getvalue())
            self.assertEqual(engine.integration_method, 'rk4')


    def test_calculate_all_forces_at_state(self):
        """Test the calculation of net forces on all bodies."""
        # Create mock bodies
        mock_body_A = MagicMock(spec=CelestialBody)
        mock_body_A.name = "A"
        mock_body_A.position = [0,0,0] # Will be overridden by temp_states

        mock_body_B = MagicMock(spec=CelestialBody)
        mock_body_B.name = "B"
        mock_body_B.position = [1,0,0] # Will be overridden by temp_states

        # Define temporary states (positions and velocities) for the bodies
        # For force calculation, only positions matter here.
        temp_states = {
            mock_body_A: ([0.0, 0.0, 0.0], [0,0,0]), # Body A at origin
            mock_body_B: ([1.0, 0.0, 0.0], [0,0,0])  # Body B at x=1
        }

        # Mock the calculate_gravitational_force method for each body
        # Force on A by B should be in +x direction
        # Force on B by A should be in -x direction
        # Magnitudes should be equal
        force_magnitude_on_A_by_B = [10.0, 0.0, 0.0]
        force_magnitude_on_B_by_A = [-10.0, 0.0, 0.0]

        mock_body_A.calculate_gravitational_force = MagicMock(return_value=force_magnitude_on_A_by_B)
        mock_body_B.calculate_gravitational_force = MagicMock(return_value=force_magnitude_on_B_by_A)

        engine = SimulationEngine([mock_body_A, mock_body_B], base_time_step=0.1)

        # Call the method to test
        all_forces = engine._calculate_all_forces_at_state(temp_states)

        # Assertions
        # Check that calculate_gravitational_force was called correctly
        # Body A calculates force from B
        mock_body_A.calculate_gravitational_force.assert_called_once_with(mock_body_B)
        # Body B calculates force from A
        mock_body_B.calculate_gravitational_force.assert_called_once_with(mock_body_A)

        # Check the net forces calculated
        self.assertEqual(all_forces[mock_body_A], force_magnitude_on_A_by_B)
        self.assertEqual(all_forces[mock_body_B], force_magnitude_on_B_by_A)

        # Verify original positions are restored (important for _calculate_all_forces_at_state)
        # This test assumes initial positions were something different, or we can set them.
        mock_body_A.position = [-100,-100,-100] # Set a known original position
        mock_body_B.position = [100,100,100]   # Set a known original position
        engine_pos_test = SimulationEngine([mock_body_A, mock_body_B], base_time_step=0.1)
        engine_pos_test._calculate_all_forces_at_state(temp_states) # This call uses temp_states
        self.assertEqual(mock_body_A.position, [-100,-100,-100]) # Should be restored
        self.assertEqual(mock_body_B.position, [100,100,100])   # Should be restored


if __name__ == '__main__':
    # Initialize Pygame font module if running tests directly and Pygame is available
    # Not strictly needed for these engine tests if CelestialBody is fully mocked,
    # but good practice if any part indirectly touches Pygame init.
    try:
        import pygame
        pygame.font.init() # Ensure font system is active for any text rendering in tested code.
    except ImportError:
        pass # Pygame not available, skip init.
    unittest.main()
