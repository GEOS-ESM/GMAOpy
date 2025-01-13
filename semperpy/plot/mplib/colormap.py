import math
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors
#import matplotlib.mpl as mpl
import matplotlib as mpl
from matplotlib.ticker import ScalarFormatter
from semperpy.core.format import float10Power, floatFormat, roundInteger, bigNumber
from semperpy.directive.directive import Directive

class ColorMap(Directive):

    def __init__(self,*args,**kargs):
        self.previous_cmap_ = None
        self.initialised_ = False
        super(ColorMap,self).__init__(*args,**kargs)

    def process(self):
        self.initialised_ = True
        min = self.min_
        max = self.max_
        if self['scale'] == 'log':
            self.norm_ = colors.LogNorm(min,max)
        else:
            self.norm_ = colors.Normalize(min,max)
        name = self['cmap']
        self.cmap_ = cm.get_cmap(name)
        if self.cmap_ is None:
            raise RuntimeError('The color map request: "%s" was not found' % name)
        # we also load the reversed cmap, depending on the stats we might one or the other
        if name[-2:] == '_r':
            name = name[0:-2]
        else:
            name += '_r'
        self.r_cmap_ = cm.get_cmap(name)
        if self.r_cmap_ is None:
            self.r_cmap_ = self.cmap_
         

    def color(self,value,moreIsBetter):
        if moreIsBetter:
            self.previous_cmap_ = self.r_cmap_
            return self.r_cmap_(self.norm_(value))
        else:
            self.previous_cmap_ = self.cmap_
            return self.cmap_(self.norm_(value))

    def draw(self,layout,subplot):
        if not self.initialised_:
            return
        if not self['display']:
            return
        rect = self['rect']
        rect,ax = layout.claimNewAxes(subplot,rect,right = 0.05)
        min = self.min_
        max = self.max_
        step = self.step_
        if step == None:
            if self['scale'] == 'log':
                print('no step and log scale')
                prev_tick = max
                ticks = [max]
                while prev_tick != 0:
                    prev_tick = prev_tick / 10.0
                    if prev_tick == min:
                        ticks = [min] + ticks
                        prev_tick = 0
                    else:
                        ticks = [prev_tick] + ticks
        else:
            ticks = np.arange(min,max + step,step)
        if self['format'] is None:
            format = self.format(min,max)
            trueformat = self.format(self.min_,self.max_)
        else:
            format = self['format']
            trueformat = format
        cmap = self.cmap_
        if self.previous_cmap_ is not None:
            cmap = self.previous_cmap_
        ticks = [np.round(x, 10) for x in ticks]
        self.colorbar_ = mpl.colorbar.ColorbarBase(ax,
                    cmap = cmap,
                    norm = self.norm_,
                    orientation = self['orientation'],
                    ticks = ticks,
                    format = format
        )
        self.colorbar_.ax.tick_params(size=0)
        formatter = ScalarFormatter()
        if self['roundint']:
            ticks = [ roundInteger(x) for x in ticks ]
        layout.registerDrawingAction('ColorBarTextSize',subplot=subplot,ax=ax,colorbar=self.colorbar_,figure=layout.figure_,title_size=self['title_size'],tick_label_size=self['tick_label_size'],ticks=ticks)
        layout.registerDrawingAction('MakeSpaceForColorBar',priority=200,subplot=subplot,ax=ax,colorbar=self.colorbar_,figure=layout.figure_)


    def format(self,minv,maxv):
        mind = float10Power(minv)
        maxd = float10Power(maxv)
        m = max(mind,maxd)
        return floatFormat(m)

    def colorbar(self):
        return self.colorbar_


    def plotColorbarTitle(self,layout,subplot,text,title,owner):
        if not self.initialised_:
            return
        if self['display']:
            self.colorbar_.set_label(text.processText(title,owner,section='title'),size=self['title_size'])

colormap = ColorMap
