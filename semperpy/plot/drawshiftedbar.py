from semperpy.plot.curve import Curve
from semperpy.plot.drawbar import BarDrawer, Bar

class ShiftedBarDrawer(BarDrawer):

    def draw(self,layout,subplot,dimension = None,axis_name = None,owner = None,bar_width_factor = 0,edgewidth=None,**kargs):
        spread = self.collectBars(self.bars_,dimension,axis_name)
        group = max([ len(x) for x in list(spread.values())])
        bar_width_factor = 0.55
        width = self.barWidth(self.bars_,dimension,axis_name,bar_width_factor)
        edgewidth = self.edgeWidth(owner,axis_name,len(spread),edgewidth)
        lines = {}
        c = ['edge','center']
        index = 0
        off = 0.0
        obj = self.graphicalObject()
        for k,bars in list(spread.items()):
            for b in bars:
                cmap = None
                if 'colormap' in owner:
                    cmap = owner['colormap']
                line = obj.draw(b,layout,subplot,order=k,width=width,cmap=cmap,edgewidth=edgewidth,align=c[index],**kargs)
                lines[id(b._ref_)] = line
                index = 1 - index
                off += width/group
        return [ lines[id(x)] for x in self.bars_ ]

Curve.registerDrawer('shiftedbar',ShiftedBarDrawer,Bar)
'''
        width = self.barWidth(self.bars_,dimension,axis_name,bar_width_factor)
        edgewidth = self.edgeWidth(owner,axis_name,len(spread),edgewidth)
        lines = OrderedDict()
        obj = self.graphicalObject()
        off = 0.0
        incr = width / group
        count = 0
        for k,bars in spread.items():
            for b in bars:
                cmap = None
                if 'colormap' in owner:
                    cmap = owner['colormap']
                line = obj.draw(b,layout,subplot,order=k//group+off,width=width/group,cmap=cmap,edgewidth=edgewidth,align='center',**kargs)
                order = count % group
                if not order in lines:
                    lines[order] = line
                off += incr
                count += 1
            if off >= width:
                off = 0.0
        return list(lines.values())
'''
