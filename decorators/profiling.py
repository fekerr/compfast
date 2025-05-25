"""
This module provides profiling decorators.
"""
import time
import functools

def time_it(func):
  """
  A decorator that measures and prints the execution time of the decorated function.

  Args:
    func: The function to be decorated.

  Returns:
    The wrapped function.
  """
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    print(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds to execute.")
    return result
  return wrapper
