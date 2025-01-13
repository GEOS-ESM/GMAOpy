import re
from collections import defaultdict
from semperpy.core.tools import to_list, is_string, is_list, no_list
from semperpy.core.date import Date
from semperpy.core.format import float10Power
from semperpy.core.texttemplate import TextTemplate
from semperpy.core.configfile import ConfigFile
from semperpy.core.configure import Configure
from gmaopy.ods.parameter import Parameter

#---------------------------------------------------------------------------------------
# This is where data formatting for displaying titles, legends etc... happens.
# In the title, legend etc... templates (in json files), we define variables between
# <> e.g. <expver>. If the keyword is part of the directive being processed it is
# displayed, unless a method with the same name as the variable is defined here.
# That way, the normal formatting of data can be overriden and new keywords can be
# created (e.g. date_interval).
#---------------------------------------------------------------------------------------
class StatTextTemplate(TextTemplate):

    beauty_ = None
    
    def date_interval(self,key,dir):
        dates = list(to_list(dir['date']))
        dates.sort()
        dates = [ Date(x) for x in dates ]
        intervals = []
        for i in range(1,len(dates)):
            intervals.append(dates[i] - dates[i-1])
        if len(intervals) > 0:
            previous = intervals[0]
            indices = []
            for i in range(1,len(intervals)):
                if intervals[i] != previous:
                    indices.append(i)
                previous = intervals[i]
            bounds = []
            bounds.append(dates[0])
            if len(indices) > 0:
                for i in indices:
                    bounds.append(dates[i])
            bounds.append(dates[-1])
            if (len(bounds) % 2) != 0:
                raise ValueError('Mistake in the date interval algorithm')
            bounds = [ d.format('%e %b %Y') for d in bounds ]
            pairs = []
            for i in range(1,len(bounds),2):
                pairs.append('-'.join([bounds[i-1],bounds[i]]))
        else:
            pairs = [dates[0].format('%e %b %Y')]
        return ','.join(pairs)

    def date_interval_with_time(self,key,dir):
        dates = list(to_list(dir['date']))
        dates = [ Date(x) for x in dates ]
        times = set()
        for d in dates:
            times.add(d.hour())
        times = list(times)
        times.sort()
        return self.date_interval(key,dir) + ' ' + ','.join(times) + 'z'

    def date_begin(self,key,dir):
        dates = list(dir['date'])
        dates.sort()
        return dates[0]

    def date_end(self,key,dir):
        dates = list(dir['date'])
        dates.sort()
        return dates[-1]

    def month(self,key,dir):
        dates = list(to_list(dir['date']))
        collection = defaultdict(dict)
        for d in dates:
            date = Date(d)
            collection[date.year()][date.month()] = date
        years = list(collection.keys())
        result = []
        years.sort()
        for year in years:
            dates = [ collection[year][x] for x in collection[year] ]
            dates.sort()
            values = []
            text = '-'.join([ x.format('%b') for x in dates[:-1] ])
            if text != '':
                values.append(text)
            values.append(dates[-1].format('%b %Y'))
            result.append('-'.join(values))
        return ','.join(result)

    def type(self,key,dir):
        if 'type' in dir:
            t = dir['type']
            return self.beautify(key,dir,t,'title')
        else:
            return ''

    def levtype(self,key,dir):
        if 'levtype' in dir:
            lt = dir['levtype']
            return self.beautify(key,dir,lt,'title')
        else:
            return ''

    def short_domain_name(self,key,dir):
        return self.beautify(key,dir,dir['domain_name'],'abbreviated')

    def level(self,key,dir):
        if not key in dir:
            return ''
        if not 'levtype' in dir:
            return dir[key]
        levtype = no_list(dir['levtype'])
        level = dir[key]
        levels = to_list(level)
        if levtype == 'pl':
            all = []
            for level in levels:
                if float10Power(level) >= 0:
                    f = '%.0f'
                else:
                    f = '%.1f'
                all.append((f + ' hPa') % level)
            return ','.join(all)
        elif levtype == 'sfc':
            return self.beautify(key,dir,'surface','title')
        elif levtype == 'ch':
            all = []
            for level in levels:
                all.append('%d' % int(level))
            return 'ch. ' + ','.join(all)
        elif levtype == 'wl':
            all = []
            for level in levels:
                all.append('%d' % int(level))
            return 'wl. ' + ','.join(all)
        else:
            raise RuntimeError('code needs to be added for level type "%s"' % levtype)

    def expver(self,key,dir):
        if 'expver' in dir:
            exp = to_list(dir['expver'])
            if len(exp) > 1:
                return ''
            else:
                return exp[0]
        else:
            return ''

    #---------------------------------------------------------------------------------------
    # utilities
    #---------------------------------------------------------------------------------------
    def beautify(self,key,dir,value,section = None):
        if is_list(value):
            values = []
            for v in value:
                values.append(str(self._beautify(key,dir,v,section)))
            return ', '.join(values)
        else:
            return self._beautify(key,dir,value,section)

    def _beautify(self,key,dir,value,section = None):
        if self.beauty_ is None:
            self.loadBeauty()
        if section is None or not section in self.beauty_:
            return value
        if value in self.beauty_[section]:
            return self.beauty_[section][value]
        return value


    def loadBeauty(self):
        config = Configure('semperpy')
        c = ConfigFile(config.file('beauty.def','CONFIG','main'),process_coma=False)
        if len(c) == 0:
            c = ''
        self.beauty_ = c

