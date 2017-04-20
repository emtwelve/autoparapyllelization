
echo $"Building analyzee"
python setup.py build_ext --inplace

python -c 'import helloworld; helloworld.hello()'


echo $"Running parallelizer"

