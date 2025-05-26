"""
CPU Intensive Workload: Fibonacci Calculator

This script defines a CPU-intensive task by calculating a Fibonacci number
using a recursive approach. It demonstrates the usage of the @time_it and
@memory_profile_it decorators to profile the function's execution time
and memory usage.
"""
import sys
import os

# Adjust the Python path to include the root directory
# This allows direct execution of the workload script and importing from parent directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decorators.profiling import time_it, memory_profile_it

@time_it
@memory_profile_it
def calculate_fibonacci(n: int) -> int:
  """
  Calculates the nth Fibonacci number using a recursive approach.

  Args:
    n: The position in the Fibonacci sequence.

  Returns:
    The nth Fibonacci number.
  """
  if n < 0:
    raise ValueError("Input must be a non-negative integer")
  elif n <= 1:
    return n
  else:
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)

if __name__ == "__main__":
  fib_number = 30
  print(f"Calculating the {fib_number}th Fibonacci number...")
  result = calculate_fibonacci(fib_number)
  print(f"The {fib_number}th Fibonacci number is: {result}")
