#!/bin/bash

# Directory to scan (change this if needed)
SRC_DIR="./src"

# File extensions to include
EXTENSIONS=("js" "ts" "html" "css" "py")

# Run the find + wc with explicit extensions
echo "Counting lines in $SRC_DIR for extensions: ${EXTENSIONS[*]}"
find "$SRC_DIR" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.html" -o -name "*.css" -o -name "*.py" \) -exec wc -l {} + | sort -n