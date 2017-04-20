
echo $"Building analyzee"
mv setup.py tests/ & cd tests
python setup.py build_ext --inplace
python -c 'import helloworld; helloworld.hello()'
mv setup.py .. & cd ..

echo $"Running parallelizer"
python -i data_dep.py tests/simple_loop.pyx

