import copy
from semperpy.plot.plot import Plot

class ColorbarPlot(Plot):

    def draw(self,layout,subplot):
        self.setColorMap(layout,subplot)
        super(ColorbarPlot,self).draw(layout,subplot)
        self.drawColorMap(layout,subplot)

    def setColorMap(self,layout,subplot):
        if 'colormap' in self:
            cmap = self['colormap']
            if cmap['min'] is None or cmap['max'] is None:
                minv = None
                maxv = None
                for curve in self.curves_:
                    values = curve.data.colormapvalue
                    m = values.min()
                    if m != curve.data.missingValue():
                        if m < minv or minv is None:
                            minv = m
                    m = values.max()
                    for v in values:
                        if v != curve.data.missingValue():
                            if v > maxv or maxv is None:
                                maxv = v
                if minv is None:
                    minv = -0.1
                if maxv is None:
                    maxv = 0.1
            if cmap['min'] is None:
                cmap.min_ = minv
            else:
                cmap.min_ = cmap['min']
            if cmap['max'] is None:
                cmap.max_ = maxv
            else:
                cmap.max_ = cmap['max']
            if cmap['step'] is None:
                if cmap['scale'] == 'log':
                    cmap.step_ = None
                else:
                    cmap.step_ = (cmap.max_ - cmap.min_) / 10.0
            else:
                cmap.step_ = cmap['step']
            cmap.process()

    def drawColorMap(self,layout,subplot):
        if 'colormap' in self:
            self['colormap'].draw(layout,subplot)

    def plotColorbarTitle(self,layout,subplot,text,info,what):
        if 'colormap' in self:
            title = self.data.colorbartitle(what)
            if 'colorbar_title' in self:
                title = self['colorbar_title']
            self['colormap'].plotColorbarTitle(layout,subplot,text,title,info)
