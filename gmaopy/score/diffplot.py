import numpy as np
import numpy.ma as ma
from semperpy.plot.colorbarplot import ColorbarPlot
from semperpy.plot.mplib.rectangle import Rectangle
from semperpy.plot.mplib.errorbar import ErrorBar
from gmaopy.stats.statistics import Statistics

class DiffPlot(ColorbarPlot):

    def draw(self,layout,subplot, lev=0.9):
        boxes = []
        minBox = 0
        maxBox = 0
        if len(self.curves_) > 0:
            reference = self.curves_[0]
            actor = Statistics.create('score',self.curves_[0].data['statistic'])
            for i in range(1,len(self.curves_)):
                curve = self.curves_[i]
                actor = Statistics.create('score',curve.data['statistic'])
                diff, lower, upper = actor.significance(curve.data.value,reference.data.value, lev=lev)
                boxes.append((lower,upper))
                curve.data.value,pop = actor.mean(diff)
            reference.data.value = np.zeros(reference.data.value.shape[1])
            if self['significance']['type'] != "none":
                boxmode = self['significance']['type'] == 'box'
                widths = [0]
                for i in range(1,len(reference.data['step'])):
                    widths.append(reference.data['step'][i] - reference.data['step'][i-1])
                if boxmode:
                    tool = Rectangle()
                else:
                    tool = ErrorBar()
                for index,b in enumerate(boxes):
                    lower = b[0]
                    upper = b[1]
                    curve = self.curves_[index+1]
                    color = curve['graphics'].color()
                    if 'color' in self['significance']:
                        color = self['significance']['color']
                    linewidth = self['significance'][self['significance']['type']+'_'+'linewidth']
                    if linewidth is None:
                        linewidth = curve['graphics'].linewidth()
                    for i in range(len(lower)):
                        y = curve.data.value[i]
                        if boxmode:
                            y = 0
                        tool.draw(layout,subplot,reference.data['step'][i],y,widths[i],upper[i]-lower[i],color=color,linewidth=linewidth)
                        if boxmode:
                            if lower[i] < minBox: minBox = lower[i]
                            if upper[i] > maxBox: maxBox = upper[i]
                        else:
                            if lower[i] < minBox: minBox = curve.data.value[i] - lower[i]
                            if upper[i] > maxBox: maxBox = curve.data.value[i] + upper[i]
        self.minBox_ = minBox
        self.maxBox_ = maxBox
        super(DiffPlot,self).draw(layout,subplot)

    def assignMinMax(self,minv,maxv,axis,allmissing):
        if self['significance']['rescale']:
            if self.minBox_ < minv: minv = self.minBox_
            if self.maxBox_ > maxv: maxv = self.maxBox_
        return super(DiffPlot,self).assignMinMax(minv,maxv,axis,allmissing) 
diffplot = DiffPlot
