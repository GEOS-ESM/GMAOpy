#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, February 2011, claude.gibert@synopticview.com
#-------------------------------------------------------------------
import numpy as np
from semperpy.core.tools import distribute
from semperpy.slicing.arraygenerator import ArrayGenerator

class Slice2Array(object):

    def __init__(self,generator = None):
        self.array_ = None
        if generator == None:
            generator = ArrayGenerator()
        self.generator_ = generator

    def __call__(self,dimensions,variable,src,dst,meta,is_interval,**kargs):
        src = distribute(src)
        dst = distribute(dst)
        if len(src) != len(dst):
            raise ValueError('Received inconsistent slices')
        for i in range(len(src)):
            self.array_[dst[i]] = variable[src[i]]

    def preProcess(self,dimensions,variable,shape,slices,metadata):
        self.array_ = self.generator_.create(shape,variable)

    def postProcess(self,dimensions,variable,shape,slices,metadata):
        self.array_ = self.generator_.postProcess(self.array_)

    def array(self):
        return self.array_

    def squeezedArray(self):
        return np.squeeze(self.array_)
