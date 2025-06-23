# Testing Guide

This project uses Python's `unittest` framework for unit tests and `coverage.py` for measuring test coverage.

## Running Unit Tests

1.  Ensure you have `coverage` installed (it's in `requirements.txt`):
    ```bash
    pip install -r requirements.txt
    # Or: pip install coverage
    ```
2.  Navigate to the project root directory (`2506/`).
3.  Run the tests using `coverage` to also measure coverage:
    ```bash
    coverage run -m unittest discover tests
    ```
    This command will discover and run all test files (matching `test_*.py`) in the `tests/` directory.

## Viewing Test Coverage

1.  After running the tests with `coverage run ...`, generate a coverage report:
    ```bash
    coverage report -m
    ```
    This will print a summary to the console, showing coverage percentage for each file and missing line numbers.

2.  For a more detailed HTML report:
    ```bash
    coverage html
    ```
    This will create an `htmlcov/` directory. Open `htmlcov/index.html` in a web browser to view an interactive report.

## Adding New Tests

-   Create new test files in the `tests/` directory, named `test_*.py`.
-   Test classes should inherit from `unittest.TestCase`.
-   Test methods should start with `test_`.
-   Ensure that your test files can import the modules they are testing (e.g., by adjusting `sys.path` as shown in `test_vector_math.py` or by structuring the project as an installable package).
