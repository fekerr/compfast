#!/bin/bash

# Intro message
echo "Checking all MicroPython versions in the PATH..."

# Create a temporary Python script
TEMP_FILE=$(mktemp)
echo 'import sys' >> $TEMP_FILE
echo 'print(sys.version)' >> $TEMP_FILE

# Find all micropython executables in the PATH
MP_PATHS=$(whereis micropython | tr ' ' '\n' | grep '/')

# Iterate over each micropython path and check the version
for MP in $MP_PATHS; do
    if [ -x "$MP" ]; then
        echo "Version for $MP:"
        $MP $TEMP_FILE
        echo ""
    fi
done

# Clean up by removing the temporary file
rm $TEMP_FILE

