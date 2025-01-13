import os
from collections import defaultdict
from distutils.core import setup, Extension
from distutils.dir_util import mkpath, copy_tree,remove_tree
from distutils.file_util import copy_file
from distutils.sysconfig import get_python_lib
from distutils.command.sdist import sdist

class Files(object):

    def __init__(self,packages):
        self.packages_ = set()
        for package in packages:
            os.path.walk(package,self,'')

    def __call__(self,arg,dirname,names):
        if dirname[0] != '.':
            self.packages_.add(dirname)

packages = ['gmaopy','semperpy','scripts']
files = Files(packages)
numpy_include = os.path.join(get_python_lib(plat_specific=True), 'numpy','core','include','numpy')

class makeDist(sdist):

    def run(self):
        base_dir = self.distribution.get_fullname()
        base_name = os.path.join(self.dist_dir, base_dir)
        mkpath(base_name)

        # Packages
        for file in files.packages_:
            copy_tree(file,os.path.join(base_name,"src",file))

        # Root files
        copy_file(os.path.join('install','setup.py'),base_name)
        copy_file(os.path.join('install','README'),base_name)
        self.distribution.metadata.write_pkg_info(base_name)

        # Documentation
        copy_tree(os.path.join('doc','_build','html'),os.path.join(base_name,'doc'))
        copy_tree(os.path.join('doc','_build','html'),os.path.join(base_name,'doc'))

        #mkpath(os.path.join(base_name,'tests'))
        copy_tree('tests',os.path.join(base_name,'tests'))

        file = self.make_archive(base_name, 'gztar', root_dir=self.dist_dir,base_dir=base_dir, owner='u', group='g')
        remove_tree(base_name)

setup(
    cmdclass = { 'sdist': makeDist },
    name='semperpy',
    version='1.81',
    description='SemperPy libraries and application for GMAO',
    author='Claude Gibert',
    author_email='dev@synopticview.co.uk',
    ext_modules=[
        Extension('gmaopy/obs/gridded/_obs_gridder',
            ['src/gmaopy/obs/gridded/obs_gridder.c'],
            include_dirs=[numpy_include],
            libraries=[])],
    packages = files.packages_,
    package_dir = { '' : 'src'},
    package_data = {
        'gmaopy': ['*.def','*.json','Makefile'],
        'semperpy': ['*.json'],
        'scripts': ['*.def','bin/*'],
        'compute': ['*.def','*.ref'],
    },
)
