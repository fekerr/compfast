"""
This is a sample workload script.
"""
import sys
import os
import logging

# If run directly, logging might not be set up by main.py.
# This is a simple way to get a logger; more robust setup would ensure
# app_logging.setup_logging() is called if this is the entry point.
# For now, assume main.py sets it up when run via CLI.
logger = logging.getLogger(__name__)

# Adjust the Python path to include the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decorators.profiling import time_it
from modules.example_module import greet

@time_it
def sample_task():
  """
  A sample task that uses the greet function.
  """
  logger.info("Sample workload starting.")
  logger.debug("Performing sample task with greet.")
  message = greet("Workload")
  # print(message) # Replaced by logger
  logger.info("Greet message: %s", message)
  # print("Running sample workload") # Replaced by logger
  logger.info("Running sample workload task completed.")

if __name__ == "__main__":
  # If this script is run directly, logging might not be configured by main.py.
  # For standalone testing, you might want to call setup_logging here.
  # from modules.app_logging import setup_logging
  # setup_logging() # Or some default level like 'DEBUG' for testing
  logger.info("sample_workload.py executed directly.")
  sample_task()
