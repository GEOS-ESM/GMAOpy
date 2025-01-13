from semperpy.core.tools import is_tuple_or_list
from semperpy.plot.curve import Curve
from semperpy.plot.drawer import Drawer

class Line(object):

    def draw(self,obj,layout,subplot,dimension = None,axis_name = None,**kargs):
        values = obj.data.value
        axis_values = dimension.process_values(obj.data[axis_name],[obj])
        graphics = obj['graphics']
        color = graphics.color()
        mfc = color
        mec = color
        if 'markerfacecolor' in graphics:
            mfc = graphics['markerfacecolor']
        if 'markeredgecolor' in graphics:
            mec = graphics['markeredgecolor']
        if graphics.horizontal():
            b = subplot.plot(values,axis_values,graphics.marker(),color=color,linestyle = graphics.style(),alpha = graphics.alpha(),linewidth = graphics.linewidth(),markersize=graphics.markersize(),markerfacecolor=mfc,markeredgecolor=mec),
        else:
            b = subplot.plot(axis_values,values,graphics.marker(),color=graphics.color(),linestyle = graphics.style(),alpha = graphics.alpha(),linewidth = graphics.linewidth(),markersize=graphics.markersize(),markerfacecolor=mfc,markeredgecolor=mec)
        while is_tuple_or_list(b):
            b = b[0]
        return b

class LineDrawer(Drawer):

    def __init__(self,klass,lines):
        self.lines_ = lines
        super(LineDrawer,self).__init__(klass)

    def draw(self,layout,subplot,dimension = None,axis_name = None,owner = None,**kargs):
        lines = []
        obj = self.graphicalObject()
        for line in self.lines_:
            lines.append(obj.draw(line,layout,subplot,dimension,axis_name,**kargs))
        return lines

Curve.registerDrawer('line',LineDrawer,Line)
