import numpy as np
from semperpy.plot.curve import Curve
from semperpy.plot.drawbar import BarDrawer, Bar

class StackedBarDrawer(BarDrawer):

    def draw(self,layout,subplot,dimension = None,axis_name = None,owner = None,bar_width_factor = 0,edgewidth=None,**kargs):
        spread = self.collectBars(self.bars_,dimension,axis_name)
        width = self.barWidth(self.bars_,dimension,axis_name,bar_width_factor)
        edgewidth = self.edgeWidth(owner,axis_name,len(spread),edgewidth)
        lines = {}
        obj = self.graphicalObject()
        for k,bars in list(spread.items()):
            previous = 0
            for b in bars:
                cmap = None
                if 'colormap' in owner:
                    cmap = owner['colormap']
                line = obj.draw(b,layout,subplot,bottom = previous,order=k,width=width,cmap=cmap,edgewidth=edgewidth,**kargs)
                previous += b.data.value[0]
                lines[id(b._ref_)] = line
        return [ lines[id(x)] for x in self.bars_ ]

    def calculateMinMax(self,bardata):
        minv = None
        maxv = None
        # start with an identical array set to 0
        values = bardata[0].value - bardata[0].value
        missing_value = bardata[0].missingValue()
        for data in bardata:
            v = data.value
            for i in range(len(values)):
                val = v[i]
                if val != missing_value:
                    values[i] += val
        for v in values:
            if minv is None or v < minv:
                minv = v
            if maxv is None or v > maxv:
                maxv = v
        allmissing = minv is None
        return minv,maxv,allmissing

Curve.registerDrawer('stackedbar',StackedBarDrawer,Bar)
