from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
ext_modules = [
    Extension(
        "pardblfine",
        ["pardblfine.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    )
]
setup(
    name='par-dblfine',
    ext_modules = cythonize("pardblfine.pyx")
)
