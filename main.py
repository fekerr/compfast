"""
JULES CLI Entry Point

This script serves as the main entry point for the JULES command-line interface.
It uses argparse to handle command-line arguments and subcommands, allowing users
to run workloads, manage configurations, and perform other operations.
"""
import argparse
import subprocess
import os

def main():
    """
    Main function for the JULES CLI.
    Handles command-line arguments and dispatches to appropriate functions.
    """
    parser = argparse.ArgumentParser(description="JULES CLI - A command-line tool for running workloads and other tasks.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging (not yet implemented).")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the run_workload command
    run_parser = subparsers.add_parser("run_workload", help="Run a specified workload script.")
    run_parser.add_argument("workload_name", help="The name of the workload script to run (e.g., sample_workload).")

    args = parser.parse_args()

    if args.command == "run_workload":
        workload_script_name = f"{args.workload_name}.py"
        workload_path = os.path.join("workloads", workload_script_name)

        try:
            if not os.path.exists(workload_path):
                raise FileNotFoundError(f"Workload script not found: {workload_path}")

            print(f"Executing workload: {workload_path}")
            # We use sys.executable to ensure we're using the same Python interpreter
            # that's running main.py
            result = subprocess.run([sys.executable, workload_path], capture_output=True, text=True, check=True)
            print("Workload output:\n", result.stdout)
            if result.stderr:
                print("Workload errors:\n", result.stderr)

        except FileNotFoundError as e:
            print(f"Error: {e}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing workload '{args.workload_name}':")
            print("Return code:", e.returncode)
            print("Output:\n", e.stdout)
            print("Errors:\n", e.stderr)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif args.verbose:
        # This is just a placeholder for now.
        # In a real application, you would initialize your logging system here.
        print("Verbose logging enabled (placeholder).")
        print("CLI entry point (verbose)")
    else:
        # If no command is specified, print help.
        # This behavior can be changed by setting a default subparser or handler.
        if args.command is None:
             print("CLI entry point. No command provided, printing help.")
             parser.print_help()
        else:
             print(f"CLI entry point. Command: {args.command}")


if __name__ == "__main__":
    # Ensure sys is imported if not already, for sys.executable
    import sys
    main()
