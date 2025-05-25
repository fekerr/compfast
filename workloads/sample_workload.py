"""
This is a sample workload script.
"""
import sys
import os

# Adjust the Python path to include the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decorators.profiling import time_it
from modules.example_module import greet

@time_it
def sample_task():
  """
  A sample task that uses the greet function.
  """
  message = greet("Workload")
  print(message)
  print("Running sample workload")

if __name__ == "__main__":
  sample_task()
