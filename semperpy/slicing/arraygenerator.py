#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, February 2011, claude.gibert@synopticview.com
#-------------------------------------------------------------------
import numpy as np
import numpy.ma as ma

class ArrayGenerator(object):

    def __init__(self,missing_value = 1.0E15,data_type = np.float64,masked = True):
        self.missing_value_ = missing_value
        self.data_type_ = data_type
        self.masked_ = masked

    def create(self,shape,source = None):
        if self.masked_:
            if source is not None:
                try:
                    self.missing_value_ = source.missing_value
                except AttributeError:
                    pass
            arrays = ma
        else:
            arrays = np
        array = arrays.zeros(shape,self.data_type_)
        if self.masked_:
            array += self.missing_value_
        return array

    def postProcess(self,array,squeeze = False):
        if self.masked_:
            array = ma.masked_values(array,self.missing_value_,copy=False,shrink=True)
            if squeeze:
                array = ma.squeeze(array)
        elif squeeze:
            array = np.squeeze(array)
        return array
