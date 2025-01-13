import numpy as np
import numpy.ma as ma

class OceanMasking(object):

    variables_ = set(['obs','oma','omf','xvec'])

    def __call__(self,array,name,file):
        if name in self.variables_:
            array = ma.masked_outside(array,-9000,9000,copy=False)
            mask = np.isnan(array)
            newmask = ma.mask_or(ma.getmask(array),mask)
            array.mask = newmask
            return array
        else:
            return array
