from semperpy.core.date import Date
from gmaopy.stats.statistics import statisticList
from gmaopy.help.helpsystem import HelpSystem

class StatisticHelp(object):
    
    def __init__(self,format,*args):
        pass

    def __call__(self):
        all = statisticList()
        pairs = [ "    %s: %s" % (a.ljust(8),b.ljust(30)) for a,b in all]
        empty = [' ']
        title = ['Available statistic per module:'] + empty
        d = Date()
        tail = empty + ['generated on %s' % d] + empty
        return title + pairs + tail


HelpSystem.register_module('statistics',StatisticHelp)
