# Project: Sum Program

This project contains a simple program written in C and a corresponding
`Makefile` to compile and generate assembly listings in both Intel and
AT&T syntax styles for x86 and x86-64 formats.

## **sum.c**

The `sum.c` file contains a program that calculates the sum of integers
up to a given number.

### **Code Summary**

```c
#include <stdlib.h>
#include <stdio.h>

// Number to guess: How many iterations of
// this loop can we go through in a second?

int main(int argc, char **argv) {
    // Declaration of variables
    int NUMBER, i, s;

    // Check if the correct number of arguments is provided
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <number>\n", argv[0]);
        return 1;
    }

    // Convert the first argument from string to integer
    NUMBER = atoi(argv[1]);

    // Initialize the sum 's' and iteration variable 'i'
    for (s = i = 0; i < NUMBER; ++i) {
        s += 1;  // Increment sum
    }

    // Return 0 to indicate successful execution
    return 0;
}
