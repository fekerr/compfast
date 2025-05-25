"""
Tests for the profiling decorator.
"""
import pytest
import io
import sys
import contextlib
import os

# Adjust the Python path to include the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decorators.profiling import time_it

def test_time_it_decorator():
  """
  Tests the time_it decorator from profiling.py.
  It checks if the decorator prints the execution time message.
  """
  @time_it
  def sample_function_for_testing():
    # Simulate some work
    return "Function executed"

  captured_output = io.StringIO()
  with contextlib.redirect_stdout(captured_output):
    result = sample_function_for_testing()

  output = captured_output.getvalue()

  assert result == "Function executed"
  assert "sample_function_for_testing" in output
  assert "seconds to execute" in output # Changed from "executed in" to match decorator output
  assert "took" in output # Ensure "took" is present as per the decorator's output format
  # We don't assert the exact time, just that the profiling message format is present.
