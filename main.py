"""
JULES CLI Entry Point

This script serves as the main entry point for the JULES command-line interface.
It uses argparse to handle command-line arguments and subcommands, allowing users
to run workloads, manage configurations, and perform other operations.
"""
import argparse
import subprocess
import os
import logging
from modules.app_logging import setup_logging
import toml # Added for config loading

CONFIG_FILE = "config.toml"
DEFAULT_LOG_LEVEL = "INFO"
config = {}

# Temporary logger for pre-setup messages
# This logger will use the default logging config (likely just console, level WARNING)
# until setup_logging is properly called.
# We must be careful as setup_logging might reconfigure the root logger.
# The app_logging.py ensures it removes old handlers.
_pre_setup_logger = logging.getLogger(f"{__name__}.pre_config")

try:
    with open(CONFIG_FILE, 'r') as f:
        config = toml.load(f)
    _pre_setup_logger.info(f"Successfully loaded configuration from {CONFIG_FILE}")
except FileNotFoundError:
    _pre_setup_logger.warning(f"Configuration file {CONFIG_FILE} not found. Using default settings.")
except toml.TomlDecodeError as e:
    _pre_setup_logger.error(f"Error decoding {CONFIG_FILE}: {e}. Using default settings.")
except Exception as e: # Catch any other potential errors during file reading/parsing
    _pre_setup_logger.error(f"An unexpected error occurred while loading {CONFIG_FILE}: {e}. Using default settings.")


# Setup logging using level from config, or default
log_level_from_config = config.get('log_level', DEFAULT_LOG_LEVEL).upper()
# Ensure the log level is valid, falling back to DEFAULT_LOG_LEVEL if not.
if not hasattr(logging, log_level_from_config):
    _pre_setup_logger.warning(f"Invalid log level '{log_level_from_config}' in config. Falling back to {DEFAULT_LOG_LEVEL}.")
    log_level_from_config = DEFAULT_LOG_LEVEL

setup_logging(log_level_from_config) # This will reconfigure the root logger correctly

logger = logging.getLogger(__name__) # Get logger for main.py AFTER setup_logging
logger.info("Initial configuration loaded: %s", config) # Log the full config after proper setup


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
    logger.debug("Arguments received: %s", args)

    if args.command == "run_workload":
        logger.info("Running workload: %s", args.workload_name)
        workload_script_name = f"{args.workload_name}.py"
        workload_path = os.path.join("workloads", workload_script_name)

        try:
            if not os.path.exists(workload_path):
                logger.error("Workload script %s not found.", workload_path)
                raise FileNotFoundError(f"Workload script not found: {workload_path}")

            # print(f"Executing workload: {workload_path}") # Replaced by logger
            logger.info(f"Executing workload: {workload_path}")
            # We use sys.executable to ensure we're using the same Python interpreter
            # that's running main.py
            result = subprocess.run([sys.executable, workload_path], capture_output=True, text=True, check=True)
            # print("Workload output:\n", result.stdout) # Replaced by logger
            logger.info("Workload output:\n%s", result.stdout)
            if result.stderr:
                # print("Workload errors:\n", result.stderr) # Replaced by logger
                logger.warning("Workload errors:\n%s", result.stderr)


        except FileNotFoundError:
            # print(f"Error: {e}") # Already logged above
            pass # Error already logged by logger.error
        except subprocess.CalledProcessError as e:
            # print(f"Error executing workload '{args.workload_name}':") # Replaced by logger
            logger.error(f"Error executing workload '{args.workload_name}':")
            # print("Return code:", e.returncode) # Replaced by logger
            # print("Output:\n", e.stdout) # Replaced by logger
            # print("Errors:\n", e.stderr) # Replaced by logger
            logger.error("Return code: %s", e.returncode)
            logger.error("Output:\n%s", e.stdout)
            logger.error("Errors:\n%s", e.stderr)
        except Exception as e:
            # print(f"An unexpected error occurred: {e}") # Replaced by logger
            logger.exception(f"An unexpected error occurred while running workload {args.workload_name}: {e}")


    elif args.verbose:
        # This is just a placeholder for now.
        # In a real application, you would initialize your logging system here.
        # print("Verbose logging enabled (placeholder).") # Replaced by logger
        # print("CLI entry point (verbose)") # Replaced by logger
        logger.info("Verbose logging enabled (placeholder).")
        logger.info("CLI entry point (verbose)")
    else:
        # If no command is specified, print help.
        # This behavior can be changed by setting a default subparser or handler.
        if args.command is None:
             # print("CLI entry point. No command provided, printing help.") # Replaced by logger
             logger.info("CLI entry point. No command provided, printing help.")
             parser.print_help()
        else:
             # print(f"CLI entry point. Command: {args.command}") # Replaced by logger
             logger.info(f"CLI entry point. Command: {args.command}")


if __name__ == "__main__":
    # Ensure sys is imported if not already, for sys.executable
    import sys
    main()
