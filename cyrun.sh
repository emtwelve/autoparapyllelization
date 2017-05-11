#!/bin/bash

echo -e '\033[0;49;93m' # Yellow
echo "AUTOPARAPYLLELIZATION"
if [ -z "$1" ]; then
  echo -e "\033[0;49;91m" # Red
  echo "No input supplied.  Try one of the following tests:"
  ls tests/
  exit 1
fi



cd tests/$1/



echo -e "\033[0;49;95m" # Pink
echo "Building original code in cython"
echo "from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
ext_modules = [
    Extension(
        \"$1\",
        [\"$1.pyx\"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    )
]
setup(
    name='$1',
    ext_modules = cythonize(\"$1.pyx\")
)" > setup.py
python setup.py build_ext --inplace



echo -e "\033[0;49;32m" # Green
echo "Building parallelized code in cython"
echo "from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
ext_modules = [
    Extension(
        \"par$1\",
        [\"par$1.pyx\"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    )
]
setup(
    name='par-$1',
    ext_modules = cythonize(\"par$1.pyx\")
)" > parsetup.py
python parsetup.py build_ext --inplace

echo -e "\033[0;49;91m" # Red
echo "Running original analyzee"
python -c 'from datetime import datetime;startTime = datetime.now();import '$1';print datetime.now() - startTime'


echo -e "\033[0;49;32m" # Green
echo "Running parallelized analyzee"
python -c 'from datetime import datetime;startTime = datetime.now();import par'$1';print datetime.now() - startTime'



rm -rf build/
rm $1.c setup.py par$1.c parsetup.py *.so
cd ../..

echo -e "\033[0;49;96m" # Cyan
echo "Running parallelizer"
#python -i data_dep.py tests/$1/$1.pyx

# Revert terminal colors to default:
tput sgr0
