"""
This module provides profiling decorators for time and memory usage.
"""
import time
import functools
import sys # For stderr

try:
    from memory_profiler import memory_usage
    MEMORY_PROFILER_AVAILABLE = True
except ImportError:
    MEMORY_PROFILER_AVAILABLE = False
    # We can't use memory_usage if it's not importable, so we'll define a placeholder.
    # The decorator will check MEMORY_PROFILER_AVAILABLE.
    def memory_usage(*args, **kwargs): # type: ignore
        # This placeholder will not be called if MEMORY_PROFILER_AVAILABLE is False.
        # It's here to satisfy type checkers or linters if they try to analyze
        # the code path where memory_profiler might be missing.
        raise NotImplementedError("memory_profiler is not installed.")

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

def memory_profile_it(func):
  """
  A decorator that measures and prints the memory usage of the decorated function.
  It uses 'memory_profiler' if available.

  Prints:
    - Function name
    - Memory usage before execution (MiB)
    - Memory usage after execution (MiB)
    - Difference in memory usage (MiB)
  
  If 'memory_profiler' is not installed, it prints a warning and does not profile memory.
  """
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    if not MEMORY_PROFILER_AVAILABLE:
      print(f"Warning: memory_profiler not installed. Cannot profile memory for '{func.__name__}'.", file=sys.stderr)
      return func(*args, **kwargs)

    # memory_profiler's memory_usage function can take a callable and its arguments directly
    # or it can be used to get memory at specific points.
    # To get before/after, we'll call it to get current memory, then run the function, then get current memory again.
    # However, memory_usage is designed to run the function itself for more accurate peak memory.
    # Let's use the recommended way: (proc_id, (func, args, kwargs))
    # For a simpler before/after snapshot without running the function *through* memory_profiler's execution context:
    # mem_before = memory_usage(proc=-1, interval=0.1, timeout=None, max_usage=False)[0] # Current memory
    # result = func(*args, **kwargs)
    # mem_after = memory_usage(proc=-1, interval=0.1, timeout=None, max_usage=False)[0] # Current memory
    # print(
    #     f"Function '{func.__name__}': "
    #     f"Memory Before: {mem_before:.2f} MiB, "
    #     f"Memory After: {mem_after:.2f} MiB, "
    #     f"Difference: {mem_after - mem_before:.2f} MiB"
    # )
    # For more detailed profiling including peak memory during the function's execution:
    # The `memory_usage` function when given a callable directly will execute it and return
    # a list of memory samples taken during its execution. The max of these is the peak.
    # The first sample can be considered "before" (or close to it, as setup for profiling happens).
    
    # Simpler approach: get memory at points, similar to time_it
    # Get memory of current process (-1 means current process)
    mem_snapshots = memory_usage(proc=-1, interval=0.001, timestamps=False, include_children=False, retval=True, max_usage=False)
    mem_before = mem_snapshots[0] # First value is current memory usage

    result = func(*args, **kwargs)
    
    mem_snapshots_after = memory_usage(proc=-1, interval=0.001, timestamps=False, include_children=False, retval=True, max_usage=False)
    mem_after = mem_snapshots_after[0]

    print(
        f"Function '{func.__name__}': "
        f"Memory Before: {mem_before:.2f} MiB, "
        f"Memory After: {mem_after:.2f} MiB, "
        f"Difference: {mem_after - mem_before:.2f} MiB"
    )
    # If you want to capture peak memory *during* the function call, `memory_profiler` is usually
    # used by running the target function through it, e.g., `mem_usage_data = memory_usage((func, args, kwargs), retval=True)`
    # then `max(mem_usage_data[0])` would be peak. The current approach is simpler for before/after.
    return result
  return wrapper
