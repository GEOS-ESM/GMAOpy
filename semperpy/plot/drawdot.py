from semperpy.plot.curve import Curve
from semperpy.plot.drawbar import Bar,BarDrawer

class Dot(Bar):

    def draw(self,obj,layout,subplot,dimension = None,order = None,width = None,**kargs):
        if width is None:
            width = 0.85
        graphics = obj['graphics']
        value = obj.data.value
        markersize = graphics.markersize()
        if graphics.horizontal():
            b = subplot.plot(value,order,'o',color=graphics.color(),markersize=markersize)
        else:
            b = subplot.plot(order,value,'o',color=graphics.color(),markersize=markersize)
        return b

Curve.registerDrawer('dot',BarDrawer,Dot)
