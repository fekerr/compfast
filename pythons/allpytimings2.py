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
    result = subprocess.run(["whereis", name], capture_output=True,
                            text=True)
    paths = result.stdout.split()
    return [path for path in paths if path.startswith('/')
            and os.path.isfile(path)
            and os.access(path, os.X_OK)]

# Collect data
data = []
for interpreter in interpreters:
    paths = find_executables(interpreter)
    for path in paths:
        try:
            version_result = subprocess.run([path, "-c", "import sys; print(sys.version)"],
                                            capture_output=True, text=True)
            version = version_result.stdout.split()[0]
            time_result = subprocess.run(["/usr/bin/time", "-p", path,
                                          "temp_runtime_script.py"],
                                         capture_output=True, text=True)
            time_lines = time_result.stderr.splitlines()
            real_time = next(line for line in time_lines if
                             line.startswith('real')).split()[1]
            data.append({
                "Interpreter": interpreter,
                "Path": path,
                "Version": version,
                "Real Time (s)": real_time
            })
        except Exception as e:
            print(f"Error with {path}: {e}")

# Print summary in compact format
print("\nSummary of versions and runtimes:")
for index, item in enumerate(data, start=1):
    path_display = item['Path']
    if len(path_display) > 50:
        path_display = "see below"
    print(f"{index}. {item['Interpreter']:12} {item['Version']:10} "
          f"{item['Real Time (s)']:>10} {path_display}")
print("\nPaths:")
for index, item in enumerate(data, start=1):
    if len(item['Path']) > 50:
        print(f"{index}. {item['Path']}")

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

