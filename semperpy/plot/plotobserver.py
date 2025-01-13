import re
import semperpy.core.format as formatter
from semperpy.core.decorators import abstractMethod
from semperpy.directive.directive import Directive

__all__ = ['Dormant']

class PlotObserver(Directive):

    def varname(self):
        return self['varname']

    def value(self):
        return ''

    def format(self,value):
        result = None
        if 'format' in self:
            f = self['format']
            if f.rfind('%') != -1:
                result  = format % value
            else:
                try:
                    func = getattr(formatter,f)
                    result = func(value)
                except AttributeError:
                    pass
        if result is None:
            result = str(value)
        return result

    @abstractMethod
    def __call__(self,plotdata,curvedata):
        pass

class Dormant(PlotObserver):
    
    def __call__(self,plotdata,curvedata):
        pass
