from semperpy.core.date import Date
from semperpy.geo.domain import Domain
from gmaopy.help.helpsystem import HelpSystem

class Domains(object):
    
    def __init__(self,format,*args):
        pass

    def __call__(self):
        all = Domain.domains('SEMPERPY')
        names = list(all.keys())
        names.sort()
        coords = []
        for x in names:
            coord = all[x].coordinates_sn()
            coords.append('     %s :' % x.ljust(16) + ', '.join([ str(x).rjust(6) for x in coord ]))
        empty = [' ']
        title = ['Available domains (South, West, North, East):'] + empty
        d = Date()
        tail = empty + ['generated on %s' % d] + empty
        return title + coords + tail


HelpSystem.register_module('domains',Domains)
