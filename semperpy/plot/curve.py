import copy
import numpy.ma as ma
from semperpy.core.tools import specialize, classof, is_list
from semperpy.core.decorators import abstractMethod
from semperpy.plot.plotdirective import PlotDirective

class Curve(PlotDirective):

    drawers_ = {}

    def get_kind(self):
        return self['kind']
    def set_kind(self,new):
        self['kind'] = new
    kind = property(get_kind,set_kind)

    def doRetrieve(self,owner,what):
        self['plotdata'].doRetrieve(owner,what)

    def startRetrieve(self):
        self['plotdata'].startRetrieve()

    def stopRetrieve(self):
        self['plotdata'].stopRetrieve()

    def finalise(self):
        pass

    def generateLegend(self,layout,subplot,legend,text):
        return text.processText(legend,self.data,section='legend')

    def __copy__(self):
        new = super(Curve,self).__copy__()
        new['plotdata'] = copy.copy(self['plotdata'])
        return new

    @classmethod
    def registerDrawer(self,category,drawer,klass):
        self.drawers_[category] = (drawer,klass)

    @classmethod
    def createDrawer(self,category,*args,**kargs):
        if not category in self.drawers_:
            raise IndexError('Cannot find category: %s, only know: %s' % (str(category),', '.join(list(self.drawers_.keys()))))
        return self.drawers_[category][0](self.drawers_[category][1],*args,**kargs)

    def __del__(self):
        a = self.data.value
        del(a)

    def feedObservers(self,plotdata,observers):
        all = {}
        mine = self.data.get('observer',[])
        for observer in observers + mine:
            observer(plotdata,self.data)
            name = observer.varname()
            value = observer.value()
            self.data[name] = value
            all[name] = value
        return all

curve = Curve
