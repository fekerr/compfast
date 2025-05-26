"""
I/O Bound Workload: Temporary File Operations

This script simulates an I/O-bound task by performing a series of file
creation, writing, reading, and deletion operations in a temporary directory.
It demonstrates the usage of @time_it and @memory_profile_it decorators
to profile the function's execution time and memory usage.
"""
import sys
import os
import tempfile
import time

# Adjust the Python path to include the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decorators.profiling import time_it, memory_profile_it

@time_it
@memory_profile_it
def perform_file_operations():
  """
  Performs I/O-bound operations: creates, writes, reads, and deletes temporary files.
  """
  temp_dir = tempfile.mkdtemp()
  file_paths = []
  num_files = 15
  file_size = 1024  # 1KB
  data_chunk = 'x' * file_size

  print(f"Performing I/O operations in temporary directory: {temp_dir}")

  try:
    # Create and write files
    print(f"Creating and writing {num_files} files...")
    for i in range(num_files):
      file_path = os.path.join(temp_dir, f"temp_file_{i}.txt")
      file_paths.append(file_path)
      with open(file_path, 'w') as f:
        f.write(data_chunk)
      time.sleep(0.01)  # Simulate I/O wait

    # Read files
    print("Reading files...")
    for file_path in file_paths:
      with open(file_path, 'r') as f:
        _ = f.read()
      time.sleep(0.01)  # Simulate I/O wait

  finally:
    # Clean up: remove files and directory
    print("Cleaning up temporary files and directory...")
    for file_path in file_paths:
      try:
        os.remove(file_path)
      except OSError as e:
        print(f"Error removing file {file_path}: {e}", file=sys.stderr)
    try:
      os.rmdir(temp_dir)
    except OSError as e:
      print(f"Error removing directory {temp_dir}: {e}", file=sys.stderr)
    print("Cleanup complete.")

if __name__ == "__main__":
  print("Starting I/O-bound workload...")
  perform_file_operations()
  print("I/O-bound workload finished.")
