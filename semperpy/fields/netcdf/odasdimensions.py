import numpy as np
from semperpy.core.tools import to_list
from semperpy.fields.netcdf.dimension import Dimension
from semperpy.fields.netcdf.dimensions import Level, LatitudeSearch, LongitudeSearch, SortedDimension

class ODASDateDimension(Dimension):
    """
        Assumes that dates are stored lineraly: between time[0] and time[-1]
        by time[1] - time[0]. Calculates the index of a date using that
        assumption, it is much more efficient than searching the array.
    """
    def __init__(self,name,f,date,**kargs):
        super(ODASDateDimension,self).__init__(name,f,**kargs)
        self.date_ = date

    def __call__(self,values = []):
        return slice(0,1,1)

    def extract_slice(self,aslice):
        return self.date_

    def __str__(self):
        return "%8s: %d" % (self.name_,self.date_)

    def contains(self,value):
        return value == self.date_

    def long_name(self):
        return "date"

class ODASLevel(SortedDimension):
    def long_name(self):
        return "level"

class ODASLatitude(LatitudeSearch):

    def long_name(self):
        return "latitude"

class ODASLongitude(Dimension):

    def __call__(self,values):
        values = to_list(values)
        if len(values) > 2:
            raise ValueError('Longitudes should be specified as an interval given by 2 values')
        v = self.variable_[:]
        if len(values) == 0:
            return [slice(0,len(v),1)]
        for i in range(len(values)):
            if values[i] > v[-1]:
                values[i] -= 360
        if len(values) == 1:
            values.append(values[0])
        start = np.searchsorted(v,values[0],'left')
        stop = np.searchsorted(v,values[1],'right')
        if start <= stop:
            if start == stop:
                stop += 1
            return [slice(start,stop,1)]
        else:
            return [slice(0,stop,1),slice(start,len(v),1)]

    def long_name(self):
        return "longitude"

    def uses_intervals(self):
        return True
