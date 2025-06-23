# src/config_loader.py
"""
Handles loading and parsing of the TOML configuration file.

This module provides a centralized way to access configuration settings
for the orbital simulation application. It defines the path to the
configuration file and includes a function to load and parse it.
"""
import tomllib # Requires Python 3.11+
from pathlib import Path
import sys

# --- Constants ---
CONFIG_FILENAME = "config.toml"
# Dynamically constructs the path: assumes config.toml is in the same directory (src/)
CONFIG_FILE_PATH = Path(__file__).parent / CONFIG_FILENAME

# --- Functions ---
def load_config():
    """
    Loads and parses the TOML configuration file (config.toml).

    Error messages are printed to sys.stderr if the file is not found,
    cannot be parsed, or another I/O error occurs.

    Returns:
        dict: A dictionary containing the configuration values if successful.
              Returns an empty dictionary on any failure to load or parse,
              allowing the main application to use defaults or handle the absence of config.
    """
    try:
        with open(CONFIG_FILE_PATH, "rb") as f: # "rb" mode required by tomllib.load
            config_data = tomllib.load(f)
        if not config_data: # Check if the loaded config is an empty dictionary (e.g., empty file)
            print(f"WARNING: Configuration file '{CONFIG_FILE_PATH}' was found but is empty or contains no data. "
                  "Application will use default settings.", file=sys.stderr)
            return {} # Treat as effectively no config / use defaults
        return config_data
    except FileNotFoundError:
        print(f"CRITICAL ERROR: Configuration file not found at '{CONFIG_FILE_PATH}'. "
              "The application relies on this file for critical settings. "
              "Please ensure 'config.toml' exists in the 'src/' directory.", file=sys.stderr)
        return {}
    except tomllib.TOMLDecodeError as e:
        print(f"CRITICAL ERROR: Could not parse configuration file '{CONFIG_FILE_PATH}'. "
              f"There is a syntax error in the TOML file: {e}. "
              "Please check the file content and TOML formatting.", file=sys.stderr)
        return {}
    except IOError as e: # Catch other I/O errors (e.g., permission issues)
        print(f"CRITICAL ERROR: An I/O error occurred while trying to read '{CONFIG_FILE_PATH}': {e}", file=sys.stderr)
        return {}
    except Exception as e: # Catch any other unexpected errors
        print(f"CRITICAL ERROR: An unexpected error occurred while loading config '{CONFIG_FILE_PATH}': {e}", file=sys.stderr)
        return {}

if __name__ == "__main__":
    # This block is for testing the loader directly.
    print(f"Attempting to load configuration from: {CONFIG_FILE_PATH.resolve()}\n")
    config = load_config()
    if config:
        print("Configuration loaded successfully:")
        if 'display' in config: print(f"  Display Settings: {config['display']}")
        if 'simulation' in config: print(f"  Simulation Settings: {config['simulation']}")
        if 'celestial_bodies' in config: print(f"  Celestial Bodies: {len(config['celestial_bodies'])} defined.")
    else:
        print("\nConfiguration loading failed or file was empty/invalid.")
