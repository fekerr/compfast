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

from decorators.profiling import time_it, memory_profile_it, MEMORY_PROFILER_AVAILABLE

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
  assert "seconds to execute" in output
  assert "took" in output
  # We don't assert the exact time, just that the profiling message format is present.

def test_memory_profile_it_decorator():
  """
  Tests the memory_profile_it decorator from profiling.py.
  It checks if the decorator prints memory usage information or a warning.
  """
  @memory_profile_it
  def sample_function_for_memory_test():
    # Allocate some memory
    a = list(range(100000))
    return "Memory function executed"

  captured_stdout = io.StringIO()
  captured_stderr = io.StringIO()

  with contextlib.redirect_stdout(captured_stdout):
    with contextlib.redirect_stderr(captured_stderr):
      result = sample_function_for_memory_test()

  stdout_output = captured_stdout.getvalue()
  stderr_output = captured_stderr.getvalue()

  assert result == "Memory function executed"

  if MEMORY_PROFILER_AVAILABLE:
    assert "sample_function_for_memory_test" in stdout_output
    assert "Memory Before:" in stdout_output
    assert "Memory After:" in stdout_output
    assert "Difference:" in stdout_output # Based on the implementation
    assert "MiB" in stdout_output
    assert stderr_output == "" # No warning should be printed to stderr
  else:
    assert "Warning: memory_profiler not installed." in stderr_output
    assert "sample_function_for_memory_test" in stderr_output # Warning includes function name
    assert stdout_output == "" # No memory profiling output to stdout
