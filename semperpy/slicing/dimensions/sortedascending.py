#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, February 2011, claude.gibert@synopticview.com
#-------------------------------------------------------------------
import numpy as np
from semperpy.core.tools import to_list, is_list, is_dict
from semperpy.slicing.dimensions.dimension import Dimension

"""
    Values are assumed to be stored in ascending order (e.g. irregular latitudes)
    A binary search algorithm is used to find the nearest value to (numpy.searchsorted)
    a specified value, faster then a sequencial search like Dimension.
    For intervals {a:b}, the slice returned include all values >= a and <= b.
    For lists [a,b,c,d], if the actual values are not in the dimension, the index of the value 
    nearest to the requested value is returned.
"""

class SortedAscendingDimension(Dimension):

    def __init__(self,*args,**kargs):
        super(SortedAscendingDimension,self).__init__(*args,**kargs)
        self.search_array_ = self.variable_[:]

    def __call__(self,values,is_interval):
        length = len(self.variable_)
        values = to_list(values)
        if is_interval:
            start = np.searchsorted(self.search_array_,values[0],'left')
            stop = np.searchsorted(self.search_array_,values[1],'right')
            if stop == length:
                stop -= 1
            if start > 0 and self.search_array_[start] > values[0]:
                start -= 1
            if stop > 0 and self.search_array_[stop-1] == values[1]:
                stop -= 1
            return [slice(start,stop+1,1)]
        else:
            found = []
            for value in values:
                if not value in self:
                    raise IndexError('value %f was not found in dimension %s' % (value,self.name_))
                i = np.searchsorted(self.search_array_,value,'left')
                if i > 0:
                    d1 = self.search_array_[i] - value
                    d2 = value - self.search_array_[i-1]
                    if d2 <= d1:
                        i = i - 1
                found.append(slice(i,i+1,1))
            return found

    def contains(self,value):
        return value <= self.search_array_[-1] and value >= self.search_array_[0]
