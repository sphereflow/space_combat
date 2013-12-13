from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
setup(name = 'math_3d', ext_modules = cythonize("math_3d.pyx"),)
setup(name = 'billboard', ext_modules = cythonize("billboard.pyx"),)
