#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, February 2011, claude.gibert@synopticview.com
#-------------------------------------------------------------------
import numpy as np
from semperpy.core.tools import to_list, is_list, is_dict
from semperpy.slicing.dimensions.dimension import Dimension

"""
    Values are assumed to be stored in descending order (e.g. pressure levels)
    A binary search algorithm is used to find the nearest value to (numpy.searchsorted)
    a specified value, faster then a sequencial search like Dimension.
    For intervals {a:b}, the slice returned include all values >= a and <= b.
    For lists [a,b,c,d], if the actual values are not in the dimension, the index of the value 
    nearest to the requested value is returned.
"""

class SortedDescendingDimension(Dimension):

    def __init__(self,*args,**kargs):
        super(SortedDescendingDimension,self).__init__(*args,**kargs)
        v = self.variable_[:]
        self.search_array_ = np.sort(v)

    def __call__(self,values,is_interval):
        length = self.len_
        values = to_list(values)
        if is_interval:
            start = length - np.searchsorted(self.search_array_,values[0],'left') - 1
            stop = length - np.searchsorted(self.search_array_,values[1],'right')
            if stop == length:
                stop -= 1
            if start > 0 and self.variable_[start] < values[0]:
                start -= 1
            if stop > 0 and self.variable_[stop-1] == values[1]:
                stop -= 1
            if start >= length:
                raise IndexError('value %f was not found in dimension %s' % (values[0],self.name_))
            return [slice(start,stop+1,1)]
        else:
            found = []
            for value in values:
                i = length - np.searchsorted(self.search_array_,value,'left') - 1
                if i > 0:
                    d1 = self.variable_[i-1] - value
                    d2 = value - self.variable_[i]
                    if d1 < d2:
                        i = i - 1
                if i < 0:
                    raise IndexError('value %f was not found in dimension %s' % (value,self.name_))
                found.append(slice(i,i+1,1))
            return found

    def contains(self,value):
        v = self.search_array_
        return value <= v[-1] and value >= v[0]
