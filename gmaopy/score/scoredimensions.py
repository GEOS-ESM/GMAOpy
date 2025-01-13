from matplotlib.ticker import ScalarFormatter
from semperpy.plot.dimension import Dimension

class MeanPlotDimension(Dimension):

    def process_values(self,values,*args):
        return values

    def process_axis(self,layout,subplot,axis,values,curves):
        print('inside ./gmaopy/score/scoredimensions.py')
        values.sort()
        axis.min(values[0])
        axis.max(values[-1])
        previous = values[0]
        vals = list(values)
        sample = set()
        for i in range(1,len(vals)):
            sample.add(vals[i] - vals[i-1]) 
        #print('sample')
        #print(sample)
        value = sample.pop()
        mod = 1
        if value < 12:
            mod = 2
        newvals = []
        for i in range(len(vals)):
            if i % mod == 0:
                newvals.append(vals[i] / 24.0)
            else:
                newvals.append('')
        labels = [ str(x) for x in newvals ]
        axis(layout,subplot,labels=labels,ticks=values)

class DiffPlotDimension(MeanPlotDimension):
    pass

class DiffPlotYDimension(MeanPlotDimension):

    def process_axis(self,layout,subplot,axis,values,curves):
        formatter = ScalarFormatter(useMathText = True,useOffset = False)
        formatter.set_powerlimits((-1,5))
        axis(layout,subplot,formatter = formatter)

Dimension.register('step','meanplot',MeanPlotDimension)
Dimension.register('step','diffplot',DiffPlotDimension)
Dimension.register('','diffplot',DiffPlotYDimension)
