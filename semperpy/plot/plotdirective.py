from semperpy.directive.directive import Directive
from semperpy.core.tools import classname

class PlotDirective(Directive):

    def get_plotdata(self):
        return self['plotdata']
    def set_plotdata(self,new):
        self['plotdata'] = new
    data = property(get_plotdata,set_plotdata)

    def __init__(self,*args,**kwargs):
        super(PlotDirective,self).__init__(*args,**kwargs)
        self.me_ = classname(self).lower()

    def me(self):
        return self.me_
