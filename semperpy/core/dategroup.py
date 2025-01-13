from collections import defaultdict
from semperpy.core.tools import sortedMappingIterator
from semperpy.core.date import Date

class DateGroup(object):

    factory_ = {}

    class Iterator(object):

        def __init__(self,group):
            self.group_ = group
            self.keys_ = sorted(group.keys())

        def __iter__(self):
            self.index_ = 0
            return self

        def __next__(self):
            if self.index_ < len(self.group_):
                value = self.group_[self.keys_[self.index_]]
                self.index_ += 1
                return sortedMappingIterator(value)
            else:
                raise StopIteration

    def __init__(self,all = None,count = 1):
        self.group_ = defaultdict(dict)
        self.count_ = count
        if all is not None:
            # try to see if it's dict otherwise assumes it is a sequence
            try:
                getattr(all,'items')
                for k,v in list(all.items()):
                    self.add(k,v)
            except AttributeError:
                for k in all:
                    self.add(k,None)


    def add(self,date,what):
        hash = self.hash(date)
        self.group_[hash][Date(date).intvalue()] = what

    def __str__(self):
        display = []
        keys = list(self.group_)
        keys.sort()
        for key in keys:
            dates = list(self.group_[key].keys())
            dates.sort()
            sub = []
            for date in dates:
                sub.append('%s - %s' % (Date(date).format(), str(self.group_[key][date])))
            display.append(', '.join(sub))
        return '\n'.join(display)

    def __iter__(self):
        self.keys_ = sorted(self.group_.keys())
        self.index_ = 0
        return self

    def __next__(self):
        if self.index_ < len(self.group_):
            value = self.group_[self.keys_[self.index_]]
            self.index_ += 1
            return value
        else:
            raise StopIteration

    def iterator(self):
        return self.Iterator(self.group_)

    @classmethod
    def registerGroup(self,name,klass):
        self.factory_[name] = klass

    @classmethod
    def createGroup(self,name,*args,**kargs):
        return self.factory_[name](*args,**kargs)

class HourGroup(DateGroup):
    def hash(self,date):
        return Date(date).hour()

class DayGroup(DateGroup):
    def hash(self,date):
        return Date(date).day()

class MonthGroup(DateGroup):
    def hash(self,date):
        return Date(date).month()

class YearGroup(DateGroup):
    def hash(self,date):
        return Date(date).year()

class HourlyGroup(DateGroup):
    def hash(self,date):
        date = Date(date)
        return date.format("%Y%m%d") + '%05d' % (int(date.hour()) // self.count_)

class DailyGroup(DateGroup):
    def hash(self,date):
        date = Date(date)
        return date.format("%Y%m") + '%05d' % ((int(date.day()) - 1) // self.count_)

class MonthlyGroup(DateGroup):
    def hash(self,date):
        date = Date(date)
        return date.format("%Y") + '%05d' % (int(date.month()) // self.count_ - 1)

class YearlyGroup(DateGroup):
    def hash(self,date):
        date = Date(date)
        return '%05d' % (int(date.year()) // self.count_)

DateGroup.registerGroup('hour',HourGroup)
DateGroup.registerGroup('day',DayGroup)
DateGroup.registerGroup('month',MonthGroup)
DateGroup.registerGroup('year',YearGroup)
DateGroup.registerGroup('hourly',HourlyGroup)
DateGroup.registerGroup('daily',DailyGroup)
DateGroup.registerGroup('monthly',MonthlyGroup)
DateGroup.registerGroup('yearly',YearlyGroup)
