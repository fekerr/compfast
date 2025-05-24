#!/usr/bin/env python

# Number to guess: How many iterations of an
# empty loop can we go through in a second?

def f(NUMBER):
    for _ in range(NUMBER):                     # python2 "xrange", python3 "range"
        pass

import sys
f(1000*int(sys.argv[1]))
