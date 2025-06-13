"""
Tests for the example_module.
"""
import sys
import os

# Adjust the Python path to include the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.example_module import greet

def test_greet():
  """
  Tests the greet function from example_module.
  """
  assert greet("Test") == "Hello, Test!"
  assert greet("World") == "Hello, World!"
  assert greet("") == "Hello, !"
