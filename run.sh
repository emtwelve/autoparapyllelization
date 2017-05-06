
#echo $"Building analyzee"
#mv setup.py tests/ & cd tests
#python setup.py build_ext --inplace
#python -c 'import helloworld; helloworld.hello()'
#mv setup.py .. & cd ..

if [ -z "$1" ]; then
  echo "No input supplied.  Try one of the following tests:"
  ls tests/
  exit 1
fi


echo $"Running parallelizer"
python -i data_dep.py tests/$1/$1.pyx

