#!/usr/bin/env python3
# 20250103 fekerr & copilot
# check runtimes of all pythons found on the system, including circuitpython and micropython

import os
import subprocess
import pandas as pd
import json
import pyarrow as pa
import pyarrow.parquet as pq

# Create a temporary Python script to measure runtime
temp_script = """
import time
start_time = time.time()
for _ in range(1000):
    pass
end_time = time.time()
print(end_time - start_time)
"""

# Write the temp script to a file
with open("temp_runtime_script.py", "w") as f:
    f.write(temp_script)

# List of possible interpreters
interpreters = ["python", "python3", "pypy", "micropython", "circuitpython"]

# Function to find all executables
def find_executables(name):
    result = subprocess.run(["whereis", name], capture_output=True, text=True)
    paths = result.stdout.split()
    return [path for path in paths if path.startswith('/') and os.path.isfile(path) and os.access(path, os.X_OK)]

# Function to get version
def get_version(interpreter, path):
    result = subprocess.run([path, "-c", "import sys; print(sys.version)"], capture_output=True, text=True)
    version_lines = result.stdout.splitlines()
    version = version_lines[0] if version_lines else "Unknown Version"
    return version

# Collect data
data = []
paths_list = []
for interpreter in interpreters:
    paths = find_executables(interpreter)
    for path in paths:
        try:
            version = get_version(interpreter, path)
            time_result = subprocess.run(["/usr/bin/time", "-p", path, "temp_runtime_script.py"], capture_output=True, text=True)
            time_lines = time_result.stderr.splitlines()
            real_time = next(line for line in time_lines if line.startswith('real')).split()[1]
            if interpreter in ["micropython", "circuitpython"]:
                version_split = version.split(";")
                display_name = version_split[1].strip()
                version = version_split[0].strip()
            else:
                display_name = interpreter
            data.append({
                "Interpreter": display_name,
                "Path": path,
                "Version": version,
                "Real Time (s)": real_time
            })
            paths_list.append(path)
        except Exception as e:
            print(f"Error with {path}: {e}")

# Print summary in compact format
print("\nSummary of versions and runtimes:")
for index, item in enumerate(data, start=1):
    print(f"{index}. {item['Interpreter']:35} {item['Version']:40} {item['Real Time (s)']:>10}")

# Print paths list
print("\nPaths:")
for index, path in enumerate(paths_list, start=1):
    print(f"{index}. {path}")

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("allpytimings.csv", index=False)

# Save to Excel
df.to_excel("allpytimings.xlsx", index=False)

# Save to JSON
with open("allpytimings.json", "w") as f:
    json.dump(data, f, indent=4)

# Save to Parquet
table = pa.Table.from_pandas(df)
pq.write_table(table, "allpytimings.parquet")

# Clean up
os.remove("temp_runtime_script.py")

print("\nData collected and saved in CSV, Excel, JSON, and Parquet formats.")

