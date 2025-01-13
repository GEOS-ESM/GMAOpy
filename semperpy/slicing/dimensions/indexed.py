#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, February 2011, claude.gibert@synopticview.com
#-------------------------------------------------------------------
import copy
import numpy as np
from semperpy.core.tools import is_dict, to_list
from semperpy.slicing.dimensions.dimension import Dimension

class IndexedDimension(Dimension):

    """
        Assumes that the values in the dimension are sorted and spaced
        equally. That way, knowing the min, max and increment, the index
        of a value can be calculated instead of search, this is more 
        efficient.
        If the requested value is not in the dimension, either
        the value on its left, its right or the closest one can 
        be returned.
    """

    def __init__(self,*args,**kargs):
        super(IndexedDimension,self).__init__(*args,**kargs)
        v = self.variable_[:]
        self.min_ = v[0]
        self.max_ = v[-1]
        if self.len_ > 1:
            self.incr_ = v[1] - self.min_
        else:
            self.incr_ = 1
        self.values_ = v

    def __call__(self,values,is_interval):
        values = copy.copy(values)
        for i in range(len(values)):
            if not values[i] in self:
                raise IndexError('%s %i is outside the boundaries' % (self.name(),values[i]))
            values[i] = self.valueToCode(values[i])
        if is_interval:
            v1 = self.indice(values[0],'left')
            v2 = self.indice(values[1],'right')
            if v1 == v2:
                return [slice(v1,v1+1,1)]
            return [slice(v1,v2+1,1)]
        else:
            slices = []
            for value in values:
                v = self.indice(value,'nearest') 
                slices.append(slice(v,v+1,1))
            return slices

    def indice(self,value,where='left'):
        v = int((value - self.min_) / self.incr_)
        if where == 'right':
            if self.values_[v] < value:
                v += 1
        elif where == 'nearest':
            if v < self.len_-1:
                d1 = abs(self.values_[v] - value)
                d2 = abs(self.values_[v+1] - value)
                if d2 < d1:
                    v += 1
        if v >= self.len_:
            v = self.len_ - 1
        return int(v)

    def extract_slice(self,aslice):
        return [ self.codeToValue(x) for x in self.values_[aslice] ]

    def __contains__(self,value):
        if is_dict(value):
            v = []
            for a,b in list(value.items()):
                v += [a,b]
            value = v
        else:
            value = to_list(value)
        value = [ self.valueToCode(x) for x in value ]
        for v in value:
            if not (v <= self.values_[self.len_-1] and v >= self.values_[0]):
                return False
        return True

    def limits(self):
        return self.codeToValue(self.min_),self.codeToValue(self.max_)

    """
        Those two methods to be overriden if the values contained in self.variable_
        are not the final usable value, but it needs to be converted (e.g. dates)
    """

    def codeToValue(self,code):
        return code

    def valueToCode(self,value):
        return value
