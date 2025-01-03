#!/bin/bash

# Intro message
echo "Checking the MicroPython version..."

# Create a temporary Python script
TEMP_FILE=$(mktemp)
echo 'import sys' >> $TEMP_FILE
echo 'print(sys.version)' >> $TEMP_FILE

# Check if a path argument is provided
if [ -z "$1" ]; then
    # No argument given, use default micropython
    whereis micropython
    micropython $TEMP_FILE
else
    # Use the provided path to micropython
    "$1" $TEMP_FILE
fi

# Clean up by removing the temporary file
rm $TEMP_FILE

