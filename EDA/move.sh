#!/bin/bash

# Set input and destination folders
INPUT="/Users/nadezhdabarbashova/Documents/fmcc_EDA/timing_files"
DEST="/Users/nadezhdabarbashova/Documents/fmcc_EDA/processed"

# Create the destination folder if it doesn't exist
mkdir -p "$DEST"

# Move files with the specified extensions
find "$INPUT" -type f \( -name "*.mat" -o -name "*.tif" -o -name "*_era.txt" \) -exec mv {} "$DEST" \;

echo "✅ Moved all .mat, .tif, and _era.txt files to $DEST"
