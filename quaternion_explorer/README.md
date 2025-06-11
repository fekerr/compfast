# Quaternion Explorer Project

## Description

This project explores Gaussian primes and Quaternions. It generates Gaussian primes, uses their components to form Quaternions, filters for prime Quaternions, and then performs pairwise multiplication of these prime Quaternions as a computational task.

## Running the Project

### Main Worker

To run the main computational task, execute the following command from the root directory of this repository:

```bash
python quaternion_explorer/main_worker.py
```

### Unit Tests

To run the unit tests, execute the following command from the root directory of this repository:

```bash
python -m unittest discover quaternion_explorer/tests
```
Alternatively, you can run individual test files:
```bash
python quaternion_explorer/tests/test_gaussian_primes.py
python quaternion_explorer/tests/test_quaternions.py
python quaternion_explorer/tests/test_main_worker.py
```

## Key Files

*   `gaussian_primes.py`: Contains functions to generate Gaussian primes (`a + bi`) and a helper for primality testing of integers.
*   `quaternions.py`: Defines the `Quaternion` class, including methods for initialization, string representation, norm calculation, primality testing for Lipschitz quaternions, and multiplication.
*   `main_worker.py`: The main script that orchestrates the generation of Gaussian primes, creation and filtering of Quaternions, and the pairwise multiplication task.
*   `tests/`: This directory contains unit tests for each of the key Python files.
    *   `test_gaussian_primes.py`
    *   `test_quaternions.py`
    *   `test_main_worker.py`
