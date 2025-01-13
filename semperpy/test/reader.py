import numpy as np
from netCDF4 import Dataset
from x import SelectionVariable

class Reader(object):

    def __init__(self,filename):
        self.file_ = Dataset(filename)
        for name,variable in list(self.file_.variables.items()):
            setattr(self,name,SelectionVariable(self.file_,name))

    def compile(self,what):
        print(what)
