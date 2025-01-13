from matplotlib.ticker import ScalarFormatter
import matplotlib.dates as md
from semperpy.core.date import Date, Hour
from semperpy.core.tools import to_list

class Dimension(object):
    
    dimensions_ = {}

    def prepare_values(self,data,values):
        return values

    def process_values(self,values,*args):
        return values

    def process_axis(self,layout,subplot,axis,values,curves,**kargs):
        formatter = self.default_formatter(values)
        axis(layout,subplot,formatter = formatter,**kargs)

    def default_formatter(self,values):
        formatter = None
        if len(values) > 0:
            try:
                float(values[0])
                formatter = ScalarFormatter(useMathText = True,useOffset = False)
                formatter.set_powerlimits((-2,5))
            except TypeError:
                pass
        return formatter


    def width(self,values):
        return None

    def labels_for_float(self,values):
        ilist = [ int(x) for x in values ]
        if values == ilist:
            return ilist
        count = 0
        for x in values:
            if x < 1:
                count += 1
        if count == len(values):
            return [ "%1.2e" % x for x in values ]
        return [ "%2.1f" % x for x in values ]

    @classmethod
    def createDimensionFilter(self,name,type,*args,**kargs):
        if type is None or name in self.dimensions_:
            return self.dimensions_[name](*args,**kargs)
        else:
            n = name + '_' + type
            if n in self.dimensions_:
                return self.dimensions_[name + '_' + type](*args,**kargs)
            elif '__default__' in self.dimensions_:
                return self.dimensions_['__default__'](*args,**kargs)
            else:
                raise IndexError('Unknown values %s %s' % (name,type))

    @classmethod
    def register(self,name,type,what):
        if type is not None:
            name = name + '_' + type
        self.dimensions_[name] = what

class DateDimension(Dimension):

    def process_values(self,values,*args):
        values = [ md.date2num(Date(x).datetime()) for x in values ]
        return values

    def process_axis(self,layout,subplot,axis,values,curves):
        print('inside process_axis')
        format, major_locator, minor_locator = self.ticks(values,axis)
        axis(layout,subplot,date=True,formatter=format,maj_locator=major_locator,min_locator=minor_locator) 
        print('exiting process_axis')

    def width(self,values):
        dates = [ Date(x) for x in values ]
        h = set()
        for x in dates:
            h.add(x.hour())
        return 1.0 / len(h)

    def ticks(self,values,axis):
        values = list(values)
        values.sort()
        date_axis_min = Date(values[0])
        date_axis_max = Date(values[-1])
        delta = (Date(values[1]) - Date(values[0])) / 2
        axis['min'] = md.date2num((date_axis_min - delta).datetime())
        axis['max'] = md.date2num((date_axis_max + delta).datetime())
        date_diff = date_axis_max - date_axis_min + 1 - (2 * delta)
        maj_locator = None
        min_locator = None
        if date_diff <= 120:
            format = "%b%d %Y %H"
            min_locator = md.HourLocator(interval=1)
            maj_locator = md.HourLocator(interval=3)
        elif 120 < date_diff and date_diff <= 240:
            format = "%b%d %Y"
            min_locator = md.DayLocator(interval = 1)
            maj_locator = md.DayLocator(interval = 2)
        elif 240 < date_diff and date_diff <= 360:
            format = "%b%d %Y"
            min_locator = md.DayLocator(interval = 1)
            maj_locator = md.DayLocator(interval = 7) #7
        elif 360 < date_diff and date_diff <= 744:
            format = "%b%d %Y" # 
            min_locator = md.DayLocator(interval = 1)
            maj_locator = md.DayLocator(interval = 7) # 7
        elif 744 < date_diff and date_diff <= 2160:   # 31-90 days
            format = "%b%d %Y"
            min_locator = md.DayLocator(interval=5) #1
            maj_locator = md.DayLocator(interval=15) #7
        elif 2160 < date_diff and date_diff <= 2880:  # 90-120 days
            format = "%b%d %Y"
            min_locator = md.DayLocator(interval=5)
            maj_locator = md.DayLocator(interval=20)
        elif 2880 < date_diff and date_diff <= 8760:  # 120 days - 365 days
            format = "%Y%m"
            min_locator = md.DayLocator(interval=30)
            maj_locator = md.MonthLocator(interval=2)
        elif 8760 < date_diff and date_diff <= 17520:  # 1 - 2 years
            format = "%b %Y" #"%b %-d, %Y %Hz"
            maj_locator = md.MonthLocator(interval=3)
            min_locator = md.MonthLocator(interval=1)
        elif 17520 < date_diff and date_diff <= 43800:  # 2 - 5 years
            format = "%b%Y"
            maj_locator = md.MonthLocator(interval=6)
            min_locator = md.MonthLocator(interval=3)
        elif 43800 < date_diff and date_diff <= 87600:  # 5 -10 years
            format = "%b%Y"
            maj_locator = md.MonthLocator(interval=12)
            min_locator = md.MonthLocator(interval=3)
        elif 87600 < date_diff and date_diff <= 175200:  # 10 - 20 years
            format = "%b%Y"
            maj_locator = md.YearLocator(3)
            min_locator = md.MonthLocator(12)
        elif 175200 < date_diff and date_diff <= 262800:# 20 - 30 years
            format = "%b%Y"
            maj_locator = md.YearLocator(4)
            min_locator = md.YearLocator()
        elif date_diff > 262800:            # more than 30 years
            #format = "%b%Y"
            format = "%Y"
            min_locator = md.YearLocator(1, month=1, day=1)
            maj_locator = md.YearLocator(5, month=1, day=1)
            #min_locator = md.MonthLocator(interval = 12)
            #maj_locator = md.MonthLocator(interval = 120)
        return md.DateFormatter(format), maj_locator, min_locator

Dimension.register('__default__',None,Dimension)
Dimension.register('date',None,DateDimension)
