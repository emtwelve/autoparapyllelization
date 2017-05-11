#!/bin/bash

echo -e '\033[0;49;93m' # Yellow
echo "AUTOPARAPYLLELIZATION"
if [ -z "$1" ]; then
  echo -e "\033[0;49;91m" # Red
  echo "No input supplied.  Try one of the following tests:"
  ls tests/
  exit 1
fi

echo -e "\033[0;49;96m" # Cyan
echo "Running parallelizer"
python -i data_dep.py tests/$1/$1.pyx

# Revert terminal colors to default:
tput sgr0
