import numpy as np
from semperpy.plot.colorbarplot import ColorbarPlot
from gmaopy.stats.statistics import Statistics
from matplotlib.font_manager import FontProperties

import matplotlib.text as text

class MeanPlot(ColorbarPlot):
    
    signature_ = 0

    def draw(self,layout,subplot):
        for curve in self.curves_:
            actor = Statistics.create('score',curve.data['statistic'])

            curve.data.value,population = actor.mean(curve.data.value)

            curve.data['population'] = population
        super(MeanPlot,self).draw(layout,subplot)
        if self['display_last_curve_value']:
            id = 'meanplot_%d' % self.signature_
            for curve in self.curves_:
                text = '%f' % curve.data.value[-1]
                x = curve.data['step'][-1]
                y = curve.data.value[-1]
                t = subplot.text(x,y,text,color = curve['graphics'].color(),fontproperties=FontProperties(size='x-small'),weight='demibold',rotation=self.signature_)
                t.set_gid(id)
            self.signature_ += 1
            layout.registerDrawingAction('SpreadTextVertically',subplot = subplot,id=id,priority=10000,layout=layout)
    
meanplot = MeanPlot
