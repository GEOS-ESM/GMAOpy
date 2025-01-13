#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, February 2011, claude.gibert@synopticview.com
#-------------------------------------------------------------------
from netCDF4 import date2num, num2date
from semperpy.core.date import Date, Hour
from semperpy.slicing.dimensions.indexed import IndexedDimension

class DateDimension(IndexedDimension):

    """
        Following the CF 1.0 convention, dates are coded as a number of units
        since a given moment, the unit can be days, hours, minutes, seconds.
        Since we are here in the Netcdf workd, we expect the variable to be
        a netcdf variable which also associated meta-data, such as the 
        units for the date.
        Dates are assumed to be regularly spaced hence the inheritance from 
        IndexedDimension.
    """
    
    def __init__(self,*args,**kargs):
        super(DateDimension,self).__init__(*args,**kargs)
        self.start_ = self.values_[0]
        # [-1] does not always work with netcdf variables
        self.units_ = self.metadata('units')
        self.stop_ = self.values_[self.len_ - 1]
        try:
            start = num2date(self.start_,self.units_)
        except Exception:
            self.units_ = self.cleanup_units(self.variable_.units)

    def cleanup_units(self,units):
        l = units.split('since')
        unit = l[0]
        l[1] = l[1].strip()
        l = l[1].split(' ')
        l[0] = l[0].strip()
        H = l[1].strip()
        h,m,d = l[0].split('-')
        d = '%04d-%02d-%02d %02d:00:00' % (int(h),int(m),int(d),int(H))
        return unit + 'since ' + d

    def codeToValue(self,code):
        return Hour(num2date(code,self.units_))

    def valueToCode(self,value):
        return date2num(Date(value).datetime(),self.units_)

    def __str__(self):
        start = self.codeToValue(self.start_)
        stop = self.codeToValue(self.stop_)
        return "%8s: from %s to %s by %f" % (self.name_,start,stop,self.incr_)
