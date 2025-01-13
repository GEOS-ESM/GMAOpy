import copy
from collections import defaultdict
from matplotlib.font_manager import FontProperties
from semperpy.core.tools import is_string,substitute_variables
from semperpy.plot.curve import Curve
from semperpy.plot.drawer import Drawer
import functools

def cmp(x,y):
    if x < y:
        return -1
    elif x > y:
        return 1
    else:
        return 0


class Bar(object):

    def draw(self,obj,layout,subplot,bottom = None,dimension = None,order = None,width = None,color = None,edgewidth=None,cmap = None,align = 'center',**kargs):
        graphics = obj['graphics']
        value = obj.data.value[0]
        if color is None:
            color = graphics.color()
        if cmap is not None:
            colormapValue = obj.data.colormapvalue[0]
            color = cmap.color(colormapValue,obj.data.colorMapMoreIsBetter())
        linewidth = None
        edgecolor = None
        if 'edgecolor' in graphics:
            edgecolor = graphics.edgecolor()
        if edgewidth is not None:
            if edgewidth == 0:
               edgecolor = color 
            else:
                linewidth = graphics.edgewidth()
        if graphics.horizontal():
            if bottom is None:
                bottom = 0
            b = subplot.bar(bottom,width,value,order,orientation='horizontal',color = color,edgecolor=edgecolor,alpha = graphics.alpha(), align = align,linewidth = linewidth)
            if obj['annotation'] is not None:
                a = obj['annotation']
                a = substitute_variables(a,obj.data)
                subplot.annotate(a,(value + value / 10,order - width/3),fontproperties=FontProperties(**obj['annotation_font']))
        else:
            b = subplot.bar(order,value,width,bottom = bottom,orientation='vertical',color = color,edgecolor=edgecolor,alpha = graphics.alpha(), align = align,linewidth = linewidth)
        return b

class BarDrawer(Drawer):

    def __init__(self,klass,bars):
        self.bars_ = bars
        super(BarDrawer,self).__init__(klass)

    def collectBars(self,bars,dimension,axis_name):
        spread = defaultdict(list)
        seen = dict()
        for i,bar in enumerate(bars):
            values = bar.data.value
            colormapValue = bar.data.colormapvalue
            axis_values = dimension.process_values(bar.data[axis_name],bars)
            if len(values) != len(axis_values) and not is_string(axis_values):
                raise ValueError('the number of values (%d) in one axis (values) does not match the number of values (%d) in the other axis (%s)' % (len(values),len(axis_values),axis_name))
            if not is_string(axis_values):
                for i in range(len(axis_values)):
                    k = axis_values[i]
                    new = copy.copy(bar)
                    newdata = copy.copy(new.data)
                    value = values[i]
                    second = colormapValue[i]
                    if value == bar.data.missingValue():
                        value = 1e-20
                        second = value
                    newdata.value = [value]
                    newdata.colormapvalue = [second]
                    new.data = newdata
                    new._ref_ = bar
                    spread[k].append(new)
            else:
                new = copy.copy(bar)
                newdata = copy.copy(new.data)
                if values[0] == bar.data.missingValue():
                    values = [1e-20]
                    colormapValue = values
                newdata.value = values
                newdata.colormapvalue = colormapValue
                new.data = newdata
                new._ref_ = bar
                if axis_values in seen:
                    i = seen[axis_values]
                else:
                    seen[axis_values] = i
                spread[i].append(new)
        return spread

    def barWidth(self,bars,dimension,axis_name,bar_width_factor):
        widths = set()
        for bar in bars:
            widths.add(dimension.width(bar.data[axis_name]))
        widths = list(widths)
        width = widths[0]
        if len(widths) > 1:
            width = min(widths)
        if width is None:
            width = bar_width_factor
        else:
            width *= bar_width_factor
        return width

    def edgeWidth(self,owner,axis_name,count,edgewidth):
        # None: default edge, value or 0 means no edge
        graph = owner['graphics']
        if graph['automatic_edge']:
            if count > graph['edge_limit']:
                if 'edgewidth' in graph:
                    edgewidth = graph['edgewidth']
                else:
                    edgewidth = 0
            else:
                edgewidth = None
        return edgewidth

    def customWidth(self,owner,axis_name,count):
        width = None
        graph = owner['graphics']
        if count < graph['custom_bar_width_limit']:
           width = graph['custom_bar_width']
        return width

    def draw(self,layout,subplot,dimension = None,axis_name = None,owner = None,bar_width_factor = 0,edgewidth=None,**kargs):
        spread = self.collectBars(self.bars_,dimension,axis_name)
        width = self.barWidth(self.bars_,dimension,axis_name,bar_width_factor)
        edgewidth = self.edgeWidth(owner,axis_name,len(spread),edgewidth)
        custom_width = self.customWidth(owner,axis_name,len(spread))
        if custom_width is not None:
            width = custom_width
        if owner['graphics'].horizontal():
            b = subplot.axvline(x = 0,color='black')
        else:
            b = subplot.axhline(y = 0,color='black',linewidth=0.8)
        lines = {}
        obj = self.graphicalObject()
        for k,bars in list(spread.items()):
#            bars.sort()#self.sortBars)
            bars = sorted(bars,key=functools.cmp_to_key(self.sortBars))
            for b in bars:
                cmap = None
                if 'colormap' in owner:
                    cmap = owner['colormap']
                line = obj.draw(b,layout,subplot,order=k,width=width,cmap=cmap,edgewidth=edgewidth,**kargs)
                lines[id(b._ref_)] = line
        return [ lines[id(x)] for x in self.bars_ ]

    def sortBars(self,a,b):
        return cmp(abs(b.data.value[0]),abs(a.data.value[0]))

Curve.registerDrawer('bar',BarDrawer,Bar)
