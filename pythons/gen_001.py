import os
import argparse

# Temporary Python script to measure runtime
temp_script = """
import sys
import time
iterations = int(sys.argv[1]) * 1000
start_time = time.time()
for _ in range(iterations):
    pass
end_time = time.time()
print(end_time - start_time)
"""

def generate_test_script(script_name, content):
    with open(script_name, 'w') as f:
        f.write(content)
    print(f"Generated test script: {script_name}")

def delete_test_script(script_name):
    if os.path.exists(script_name):
        os.remove(script_name)
        print(f"Deleted test script: {script_name}")
    else:
        print(f"Test script {script_name} does not exist.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and optionally delete test scripts.")
    parser.add_argument("--generate", type=str, help="Generate a test script with the given name.")
    parser.add_argument("--delete", type=str, help="Delete the test script with the given name.")
    parser.add_argument("--content", type=str, help="Content to write into the generated test script.", default=temp_script)

    args = parser.parse_args()

    if args.generate:
        generate_test_script(args.generate, args.content)

    if args.delete:
        delete_test_script(args.delete)

