import os
from distutils.core import setup, Extension
from distutils.sysconfig import get_python_lib

numpy_include = os.path.join(get_python_lib(plat_specific=True), 'numpy','core','include','numpy')

setup(
    name='semperpy',
    version='1.61',
    description='SemperPy libraries and application for GMAO',
    author='Claude Gibert',
    author_email='dev@synopticview.co.uk',
    ext_modules=[
        Extension('gmaopy/obs/gridded/_obs_gridder',
            ['gmaopy/obs/gridded/obs_gridder.c'],
            include_dirs=[numpy_include],
            libraries=[])],
)
