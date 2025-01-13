from semperpy.plot.plotobserver import PlotObserver

__all__ = ['odscounter']

class ODSCounter(PlotObserver):

    def __init__(self,*args,**kwargs):
        self.counter_ = 0
        super(ODSCounter,self).__init__(*args,**kwargs)

    def __call__(self,plotdata,curvedata):
        variables = curvedata.variables(variable = 'all')
        keys = list(variables.keys())
        var = curvedata.variables(variable = keys[0])
        self.counter_ += len(var)

    def value(self):
        return self.format(self.counter_)

    def __copy__(self):
        new = super(ODSCounter,self).__copy__()
        new.counter_ = self.counter_
        return new

odscounter = ODSCounter
