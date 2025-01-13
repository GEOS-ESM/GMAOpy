#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, February 2011, claude.gibert@synopticview.com
#-------------------------------------------------------------------
import numpy as np
from semperpy.core.tools import to_list, is_list, is_dict

class Dimension(object):

    """
        An real / abstract class which defines the behaviour of dimension objects.
        A dimension object is in charge of one of the dimensions of a multi-dimensional
        array (e.g. a dimension in a netcdf class). These should be independent from netcdf
        so that dimension objects can be instanciated on an array in memory.
        A dimension object has:
           - a name: normally the name of the dimension e.g. the netcdf file
             to request slices of values.
           - a variable: the variable containing all the values of that dimension
        A dimension object should be able to:
           - find slices along that dimension for lists of values or intervals
           - slice into its own variable to return a subset (slice) of the values
           - return its limits (first and last values, not necessarily min and max
             if the dimension is not sorted).
    """

    def __init__(self,name,official_name,variable,metadata_handler = None):
        self.name_ = name
        self.official_name_ = official_name
        self.variable_ = variable
        self.values_ = self.variable_[:]
        self.len_ = len(self.values_)
        self.cache_ = {}
        self.metadata_handler_ = metadata_handler

    def name(self,newname = None):
        if newname:
            self.name_ = newname
        return self.name_

    def officialName(self,newname = None):
        if newname:
            self.official_name_ = newname
        return self.official_name_

    def array(self):
        return self.values_

    def metadata(self,name):
        return self.metadata_handler_(self,name)

    def slice(self,aslice):
        """
           returns a subset of the variable. Slices are cached so that if the same slice
           is requested many times, the process is faster.
        """
        h = self.hash_slice(aslice)
        if h in self.cache_:
            return self.cache_[h]
        v = self.extract_slice(aslice)
        self.cache_[h] = v
        return v
    
    def hash_slice(self,aslice):
        """
            some way of identifying a slice in a unique way.
        """
        return int("%d%d" % (aslice.start,aslice.stop))

    def extract_slice(self,aslice):
        return list(self.values_[aslice])

    def findSlice(self,values,is_interval = []):
        result = []
        if is_dict(values):
            is_interval.append(True)
            slices = []
            if len(values) == 0:
                result = [slice(0,len(self.values_),1)]
            else:
                for a,b in list(values.items()):
                    l = [a,b]
                    result += self(l,True)
        else:
            values = to_list(values)
            result += self(values,False)
            is_interval.append(False)
        return result
        

    def __call__(self,values,is_interval):
        found = []
        if is_interval:
            """
            in this case we have no guarantee that an interval makes sense, we just
            return all the values between the two values found
            """
            start = self.find(values[0])
            stop = self.find(values[1])
            return [slice(start,stop+1,1)]
        for value in values:
            i = self.find(value)
            found.append(slice(i,i+1,1))
        return found

    def __str__(self):
        v = self.values_
        if len(v) > 1:
             return "%8s: from %f to %f by %f, %d values" % (self.name_,v[0],v[-1],v[1]-v[0],len(v))
        else:
             return "%8s: %f. %d values" % (self.name_,v[0],len(v))

    def limits(self):
        v = self.values_
        if len(v) > 1:
            return v[0],v[-1]
        else:
            return v[0],v[0]

    def __contains__(self,value):
        if is_dict(value):
            v = []
            for a,b in list(value.items()):
                v += [a,b]
            value = v
        else:
            value = to_list(value)
        for v in value:
            if not self.contains(v):
                return False
        return True

    def contains(self,value):
        v = self.values_
        i = np.where(v == value)
        return len(i) > 0 and len(i[0]) > 0

    def find(self,value):
        i = np.where(self.values_ == value)
        if len(i) == 0 or len(i[0]) == 0:
            raise IndexError('value %f was not found in dimension %s' % (value,self.name_))
        return i[0][0]

