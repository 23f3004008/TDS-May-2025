#!/bin/bash

# Create main directory and extract
mkdir -p q-move-rename-files
unzip -X q-move-rename-files.zip -d q-move-rename-files
cd q-move-rename-files

# Create new folder for processed files
mkdir -p nf

# Move all files from subdirectories to nf
find . -mindepth 2 -type f -exec mv {} nf/ \;

# Go to the new folder
cd nf

# Rename files replacing digits with next number
for file in *; do
    # Skip if not a file
    [ -f "$file" ] || continue
    
    # Create new name by incrementing each digit
    newname=$(echo "$file" | sed 'y/0123456789/1234567890/')
    
    # Rename the file
    mv "$file" "$newname"
done

# Run the hash command
grep . * | LC_ALL=C sort | sha256sum 