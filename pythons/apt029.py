#!/usr/bin/env python3
# 20250103 fekerr & copilot
# Check runtimes of all pythons found on the system, including circuitpython and micropython

import os
import subprocess
import pandas as pd
import json
import pyarrow as pa
import pyarrow.parquet as pq
import math

# Ensure gen_003.py is present
gen_script = "gen_003.py"
if not os.path.exists(gen_script):
    raise FileNotFoundError(f"{gen_script} not found.")

# Generate test scripts using gen_003.py
subprocess.run(["python", gen_script, "--generate", "temp_runtime_script.py"])
subprocess.run(["python", gen_script, "--generate", "loop.py"])

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

# Function to measure runtime
def measure_runtime(path, script_name, iterations):
    result = subprocess.run(["/usr/bin/time", "-p", path, script_name, str(iterations)], capture_output=True, text=True)
    time_lines = result.stderr.splitlines()
    real_time = next(line for line in time_lines if line.startswith('real')).split()[1]
    return float(real_time)

# Collect data
data = []
paths_list = []
output_lines = []
for interpreter in interpreters:
    paths = find_executables(interpreter)
    for path in paths:
        try:
            version = get_version(interpreter, path)
            first_runtime = measure_runtime(path, "temp_runtime_script.py", 1000)
            if first_runtime == 0:
                estimated_iterations = 1000000  # Default to a high value if runtime is too fast
            else:
                estimated_iterations = int(math.ceil(1000 / first_runtime))  # Estimate iterations for ~1.0 second runtime
            
            second_runtime = measure_runtime(path, "temp_runtime_script.py", estimated_iterations)
            loop_runtime = measure_runtime(path, "loop.py", estimated_iterations)
            
            if interpreter in ["micropython", "circuitpython"]:
                version_split = version.split(";")
                interpreter_name = version_split[1].split()[0].strip()
                version_info = version_split[0].strip() + "; " + " ".join(version_split[1].split()[1:])
            else:
                interpreter_name = interpreter
                version_info = version.strip()
            
            data.append({
                "Interpreter": interpreter_name,
                "Path": path,
                "Version": version_info,
                "First Runtime (s)": first_runtime,
                "Second Runtime (s)": second_runtime,
                "Loop Runtime (s)": loop_runtime,
                "Estimated Iterations (K)": estimated_iterations
            })
            paths_list.append(path)
        except Exception as e:
            error_message = f"Error with {path}: {e}"
            print(error_message)
            output_lines.append(error_message)

# Print and save interpreter versions
version_info_lines = [
    "\nInterpreter                     Version Info",
    "===========                     ============"
]
for index, item in enumerate(data, start=1):
    line = f"{index:2}. {item['Interpreter']:<25} {item['Version']}"
    print(line)
    version_info_lines.append(line)
output_lines.extend(version_info_lines)

# Print and save runtimes
runtime_info_lines = [
    "\nRuntimes (seconds, #K loops):",
    "============================="
]
for item in data:
    line = f"{item['First Runtime (s)']:.3f}, {item['Second Runtime (s)']:.3f} ({item['Estimated Iterations (K)']}K); {item['Loop Runtime (s)']:.3f}, {item['Loop Runtime (s)']:.3f} ({item['Estimated Iterations (K)']}K)"
    print(line)
    runtime_info_lines.append(line)
output_lines.extend(runtime_info_lines)

# Print and save paths list
path_info_lines = [
    "\nPaths:"
]
for index, path in enumerate(paths_list, start=1):
    line = f"{index}. {path}"
    print(line)
    path_info_lines.append(line)
output_lines.extend(path_info_lines)

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

# Save screen output to file
with open("allpytimings.txt", "w") as f:
    f.write("\n".join(output_lines))

# Clean up test scripts using gen_003.py
subprocess.run(["python", gen_script, "--delete", "temp_runtime_script.py"])
subprocess.run(["python", gen_script, "--delete", "loop.py"])

print("\nData collected and saved in CSV, Excel, JSON, Parquet, and text formats.")
