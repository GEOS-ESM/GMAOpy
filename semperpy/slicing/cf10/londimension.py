#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, February 2011, claude.gibert@synopticview.com
#-------------------------------------------------------------------
from semperpy.slicing.dimensions.indexed import IndexedDimension

class LonDimension(IndexedDimension):
    
    def adjust_values(self,values,is_interval):
        overlap = False
        for i in range(len(values)):
            if values[i] > 180:
                values[i] -= 360
        if is_interval:
            # e.g. [0 360]
            if (values[1] == values[0]) % 360 == 0:
                overlap = True
                values[1] -= self.incr_
        return values,overlap


    def __call__(self,values,is_interval):
        values,overlap = self.adjust_values(values,is_interval)
        slices = super(LonDimension,self).__call__(values,is_interval)
        result = slices
        if is_interval:
            s = slices[0]
            # we overlap the 0
            if overlap:
                s = slice(s.start,s.start,1)
            if s.start >= s.stop:
                result = [slice(s.start,self.len_,s.step),slice(0,s.stop,s.step)]
        return result
