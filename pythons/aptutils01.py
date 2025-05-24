import os
import subprocess

def find_executables(name):
    result = subprocess.run(["whereis", name], capture_output=True, text=True)
    paths = result.stdout.split()
    return [path for path in paths if path.startswith('/') and os.path.isfile(path) and os.access(path, os.X_OK)]

def get_version(interpreter, path):
    result = subprocess.run([path, "-c", "import sys; print(sys.version)"], capture_output=True, text=True)
    version_lines = result.stdout.splitlines()
    version = version_lines[0] if version_lines else "Unknown Version"
    return version

def measure_runtime(path, script_name, iterations):
    result = subprocess.run(["/usr/bin/time", "-p", path, script_name, str(iterations)], capture_output=True, text=True)
    time_lines = result.stderr.splitlines()
    real_time = next(line for line in time_lines if line.startswith('real')).split()[1]
    return float(real_time)

