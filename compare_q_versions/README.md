# Compare Quaternion Versions (`compare_q_versions`)

This directory contains tools to compare different implementations of quaternions developed in this project.

## Files

-   `__init__.py`: Marks this directory as a Python package.
-   `compare.py`: The main script for running comparisons.

## `compare.py`

This script instantiates and compares two types of quaternions:

1.  **`OriginalQuaternion`**: From the `quaternion_explorer` module. This quaternion type uses four integer components `(a,b,c,d)`.
2.  **`GaussianIntQuaternion`**: From the `q_alpha` module. This quaternion type uses eight integer parameters `(p0, ..., p7)` which define four `IntegerGaussian` coefficients for `w, x, y, z`.

The script uses `PrimeParameterIterator` (from the `iterPrimes` module) to generate sequences of prime numbers as parameters for these quaternion types.

### Functionality

For a specified number of comparison sets, the script:
1.  Generates two sets of 4 prime parameters for `OriginalQuaternion`.
2.  Generates two sets of 8 prime parameters for `GaussianIntQuaternion`.
3.  Instantiates two instances of each quaternion type (e.g., `oq1`, `oq2` and `giq1`, `giq2`).
4.  Prints the string representations of these instances.
5.  Calculates and prints the string representation of their products (`oq1 * oq2` and `giq1 * giq2`).
6.  Prints some unique properties/method results for each type (e.g., `conjugate()` for `GaussianIntQuaternion`, `norm_squared()` and `is_prime()` for `OriginalQuaternion`).

### How to Run

To run the comparison script, navigate to the root directory of the project (the parent of `compare_q_versions`, `iterPrimes`, etc.) and execute:

```bash
python compare_q_versions/compare.py
```
Alternatively, you can run it as a module:
```bash
python -m compare_q_versions.compare
```
The script will print the comparison results to the console. You can change the number of parameter sets to test by modifying the `num_sets` variable within the `if __name__ == '__main__':` block in `compare.py`.
