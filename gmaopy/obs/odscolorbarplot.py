import numpy as np
from gmaopy.obs.odsplot import ODSPlot

class ODSColorbarPlot(ODSPlot):

    def drawColorbar(self,layout,subplot):
        if 'colormap' in self:
            self['colormap'].draw(layout,subplot)

    def setColorMap(self,layout,subplot,var):
        if 'colormap' in self:
            cmap = self['colormap']
            cmap.min_ = cmap['min']
            if cmap.min_ is None:
                cmap.min_ = np.min(var)
            cmap.max_ = cmap['max']
            if cmap.max_ is None:
                cmap.max_ = np.max(var)
            cmap.step_ = cmap['step']
            if cmap.step_ is None:
                cmap.step_ = (cmap.max_ - cmap.min_) / 10.0
            cmap.process()

    def plotColorbarTitle(self,layout,subplot,text,info,what):
        if 'colormap' in self:
            title = self.data.colorbartitle(what)
            if 'colorbar_title' in self:
                title = self['colorbar_title']
            self['colormap'].plotColorbarTitle(layout,subplot,text,title,info)
