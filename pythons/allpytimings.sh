#!/bin/bash

# Intro message
echo "Checking versions and runtimes for all Python interpreters in the PATH..."

# Create a temporary Python script
TEMP_FILE=$(mktemp)
echo 'import time' >> $TEMP_FILE
echo 'start_time = time.time()' >> $TEMP_FILE
echo 'for _ in range(1000): pass' >> $TEMP_FILE
echo 'end_time = time.time()' >> $TEMP_FILE
echo 'print("Runtime: {:.6f} seconds".format(end_time - start_time))' >> $TEMP_FILE

# Find all relevant interpreters in the PATH
INTERPRETERS=$(whereis python python3 pypy micropython | tr ' ' '\n' | grep '/')

# Iterate over each interpreter, check the version, and measure the runtime
for INTERP in $INTERPRETERS; do
    if [ -x "$INTERP" ]; then
        echo "Version for $INTERP:"
        $INTERP -c 'import sys; print(sys.version)'
        echo "Timing for $INTERP:"
        /usr/bin/time -p $INTERP $TEMP_FILE
        echo ""
    fi
done

# Clean up by removing the temporary file
rm $TEMP_FILE

