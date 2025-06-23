# src/celestial_body.py
"""
Provides the CelestialBody class for representing objects in the simulation
and utility functions for 3D vector mathematics.
"""
import math
from collections import deque
import sys

# --- 3D Vector Math Utility Functions ---
# (Docstrings were good, minor type hint style adjustments for illustration)
def vec_add(v1, v2):
    """Adds two 3D vectors. Args: v1 (list[float]), v2 (list[float]). Returns: list[float]."""
    return [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]
def vec_sub(v1, v2):
    """Subtracts v2 from v1. Args: v1 (list[float]), v2 (list[float]). Returns: list[float]."""
    return [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]
def vec_scale(v, s):
    """Scales vector v by scalar s. Args: v (list[float]), s (float). Returns: list[float]."""
    return [v[0] * s, v[1] * s, v[2] * s]
def vec_magnitude(v):
    """Calculates magnitude of vector v. Args: v (list[float]). Returns: float."""
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
def vec_normalize(v):
    """Normalizes vector v. Args: v (list[float]). Returns: list[float] (unit vector or zero vector)."""
    mag = vec_magnitude(v)
    if mag == 0: return [0.0,0.0,0.0]
    return [v[0]/mag, v[1]/mag, v[2]/mag]

class CelestialBody:
    """Represents a celestial body with physical properties and orbital path history."""
    GRAVITATIONAL_CONSTANT = 6.67430e-11  # N m^2 / kg^2

    def __init__(self, name, mass, radius, color, position, velocity, max_history=200):
        # (Docstring from previous step assumed sufficient)
        self.name = str(name)
        self.mass = float(mass)
        self.radius = float(radius)
        self.color = str(color)
        self.position = list(position)
        self.velocity = list(velocity)
        self.acceleration = [0.0, 0.0, 0.0]

        if not isinstance(max_history, int) or max_history < 0:
            print(f"Warning: Invalid max_history '{max_history}' for {self.name}. Setting to 0 (no history).", file=sys.stderr)
            self.max_history = 0
        else: self.max_history = max_history

        # maxlen=0 creates a deque that can never hold items.
        # maxlen=None creates an unbounded deque. If max_history is truly 0, no history is desired.
        self.position_history = deque(maxlen=self.max_history if self.max_history > 0 else 0)

        if self.max_history > 0 and position: # Only add initial position if history is active
            self.position_history.append(list(position))

    def __str__(self): # Unchanged from previous refactor
        return (f"Body: {self.name} | Mass: {self.mass:.2e} kg | Radius: {self.radius:.0f} km\n"
                f"  Pos (m): [{self.position[0]:.3e}, {self.position[1]:.3e}, {self.position[2]:.3e}]\n"
                f"  Vel (m/s): [{self.velocity[0]:.3e}, {self.velocity[1]:.3e}, {self.velocity[2]:.3e}]\n"
                f"  Acc (m/s^2): [{self.acceleration[0]:.3e}, {self.acceleration[1]:.3e}, {self.acceleration[2]:.3e}]")

    def calculate_gravitational_force(self, other_body): # Error handling added
        if not isinstance(other_body, CelestialBody): raise TypeError("other_body must be CelestialBody")
        if other_body is self: return [0.0,0.0,0.0]
        r_vector = vec_sub(other_body.position, self.position)
        distance_sq = r_vector[0]**2 + r_vector[1]**2 + r_vector[2]**2
        if distance_sq == 0:
            print(f"Warning: Zero distance between '{self.name}' and '{other_body.name}'. "
                  "Gravitational force calculation undefined. Returning zero force.", file=sys.stderr)
            return [0.0,0.0,0.0]
        force_magnitude = (self.GRAVITATIONAL_CONSTANT * self.mass * other_body.mass) / distance_sq
        r_unit_vector = vec_normalize(r_vector)
        return vec_scale(r_unit_vector, force_magnitude)

    def get_state_derivatives(self, temp_pos, temp_vel, net_force): # Unchanged from previous refactor
        vel_deriv = temp_vel
        if self.mass==0: acc_deriv=[0.0,0.0,0.0]
        else: acc_deriv=vec_scale(net_force,1.0/self.mass)
        return (vel_deriv,acc_deriv)

    def update_post_simulation(self): # Unchanged from previous refactor
        if self.max_history > 0: self.position_history.append(self.position[:])
