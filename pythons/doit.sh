#! /usr/bin/bash
# 20250103 fekerr & copilot
# note this loop.py multiplies the argument give by 1000

# set -x

./allmuver.sh

echo ""

/usr/bin/time micropython loop.py 1000

echo ""

/usr/bin/time /usr/bin/micropython loop.py 1000

echo ""
# which pypy
whereis pypy

pypy --version
/usr/bin/time pypy loop.py 1000

time python loop.py 1000
# set +x
