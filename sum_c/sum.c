#include <stdlib.h>
#include <stdio.h>

// Number to guess: How many iterations of
// this loop can we go through in a second?

#define GUESS 10000000

int main(int argc, char **argv) {
    // Declaration of variables
    int NUMBER = GUESS, i, s;
    printf("argc=%d\n", argc);
    if (argc < 2) {
        printf("no guess entered, using %d", NUMBER);
    } else {
        // Convert the first argument from string to integer
        printf("argv[1]=%s", argv[1]);
        NUMBER = atoi(argv[1]);
    }

    // Initialize the sum 's' and iteration variable 'i'
    for (s = i = 0; i < NUMBER; ++i) {
        s += 1;  // Increment sum
    }

    // Return 0 to indicate successful execution
    return 0;
}

