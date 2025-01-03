#!/bin/bash

# Create a temporary Python script
TEMP_FILE=$(mktemp)
echo 'import sys' >> $TEMP_FILE
echo 'print(sys.version)' >> $TEMP_FILE

# Run the temporary Python script with MicroPython
micropython $TEMP_FILE

# Clean up by removing the temporary file
rm $TEMP_FILE

