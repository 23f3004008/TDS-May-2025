#!/bin/bash

# Create directory and extract
mkdir -p q-list-files-attributes
unzip -X q-list-files-attributes.zip -d q-list-files-attributes
cd q-list-files-attributes

# Run the size calculation command
ls -l --time-style=full-iso | awk '$5 >= 6216 && $6" "$7 >= "2018-01-19 19:44:00" {total += $5} END {print total}' 