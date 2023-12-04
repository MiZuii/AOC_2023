#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <directory name>"
    exit 1
fi

mkdir "$1"
cat template.py >> "$1"/puzzle1.py
cat template.py >> "$1"/puzzle2.py
cd "$1"
touch input1.txt
touch input2.txt
