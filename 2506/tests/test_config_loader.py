# tests/test_config_loader.py
"""
Unit tests for the config_loader module.
"""
import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
import io # For capturing stderr

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import the module to test AFTER sys.path modification
import config_loader
# Import tomllib for TOMLDecodeError if not already imported by config_loader for type checking
try:
    import tomllib # Python 3.11+
except ImportError:
    # In a real scenario with older Python, you'd use 'toml' and ensure it's a dependency.
    # For this test environment, we assume tomllib is available as per project setup.
    # Creating a dummy TomlDecodeError if tomllib is not found for type hinting purposes in except block.
    class TOMLDecodeError(Exception): pass
    tomllib = MagicMock() # Mock tomllib if it's not found, tests will focus on error raising.
    tomllib.TOMLDecodeError = TOMLDecodeError


class TestConfigLoader(unittest.TestCase):
    """Test suite for config_loader.py"""

    @patch('sys.stderr', new_callable=io.StringIO) # Capture stderr
    @patch('tomllib.load') # Mock tomllib.load first
    @patch('builtins.open', new_callable=mock_open) # Then mock open
    def test_load_config_success(self, mock_file_open, mock_tomllib_load, mock_stderr):
        """Test successful configuration loading."""
        expected_config = {"display": {"width": 1920, "height": 1080}}
        mock_tomllib_load.return_value = expected_config

        # Ensure config_loader.CONFIG_FILE_PATH is used by the mocked open
        # This requires config_loader to be imported and its CONFIG_FILE_PATH to be set.
        # We assume config_loader.py sets its own CONFIG_FILE_PATH correctly.

        result = config_loader.load_config()

        mock_file_open.assert_called_once_with(config_loader.CONFIG_FILE_PATH, "rb")
        mock_tomllib_load.assert_called_once()
        self.assertEqual(result, expected_config)
        self.assertEqual(mock_stderr.getvalue(), "") # No error messages

    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('builtins.open', side_effect=FileNotFoundError("File not found for test"))
    def test_load_config_file_not_found(self, mock_file_open, mock_stderr):
        """Test FileNotFoundError during config loading."""
        result = config_loader.load_config()
        mock_file_open.assert_called_once_with(config_loader.CONFIG_FILE_PATH, "rb")
        self.assertEqual(result, {}) # Should return empty dict
        self.assertIn("CRITICAL ERROR: Configuration file not found", mock_stderr.getvalue())

    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('tomllib.load', side_effect=tomllib.TOMLDecodeError("TOML parsing error for test", "doc", 0))
    @patch('builtins.open', new_callable=mock_open)
    def test_load_config_toml_decode_error(self, mock_file_open, mock_tomllib_load, mock_stderr):
        """Test TOMLDecodeError during config loading."""
        result = config_loader.load_config()
        mock_file_open.assert_called_once_with(config_loader.CONFIG_FILE_PATH, "rb")
        mock_tomllib_load.assert_called_once()
        self.assertEqual(result, {}) # Should return empty dict
        self.assertIn("CRITICAL ERROR: Could not parse configuration file", mock_stderr.getvalue())
        self.assertIn("TOML parsing error for test", mock_stderr.getvalue())

    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('tomllib.load', return_value={}) # Simulate an empty but valid TOML file
    @patch('builtins.open', new_callable=mock_open)
    def test_load_config_empty_file(self, mock_file_open, mock_tomllib_load, mock_stderr):
        """Test loading an empty (but valid) configuration file."""
        result = config_loader.load_config()
        mock_file_open.assert_called_once_with(config_loader.CONFIG_FILE_PATH, "rb")
        mock_tomllib_load.assert_called_once()
        self.assertEqual(result, {}) # Should return empty dict
        # Check for the specific warning about an empty file
        self.assertIn("WARNING: Configuration file", mock_stderr.getvalue())
        self.assertIn("was found but is empty", mock_stderr.getvalue())


    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('builtins.open', side_effect=IOError("Generic IO error for test")) # Simulate other IO error
    def test_load_config_generic_exception(self, mock_file_open, mock_stderr):
        """Test other generic exceptions during config loading."""
        result = config_loader.load_config()
        mock_file_open.assert_called_once_with(config_loader.CONFIG_FILE_PATH, "rb")
        self.assertEqual(result, {})
        self.assertIn("CRITICAL ERROR: An unexpected error occurred", mock_stderr.getvalue())
        self.assertIn("Generic IO error for test", mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
