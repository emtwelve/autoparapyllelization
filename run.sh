
echo $"Building analyzee"
#mv setup.py .. & cd ..

echo "from distutils.core import setup
from Cython.Build import cythonize
setup(
    ext_modules = cythonize(\"$1.pyx\")
)" > tests/$1/setup.py
cd tests/$1/
python setup.py build_ext --inplace
python -c 'import '$1
rm -rf build/
rm $1.c setup.py
cd ../..

if [ -z "$1" ]; then
  echo "No input supplied.  Try one of the following tests:"
  ls tests/
  exit 1
fi


echo $"Running parallelizer"
python -i data_dep.py tests/$1/$1.pyx

