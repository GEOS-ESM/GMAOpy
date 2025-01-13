import numpy.ma as ma
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from semperpy.plot.mplib.layout import Layout
from semperpy.fields.field import Field

class Plotter(object):

    def __init__(self,layout = [1,1], scanmode = 'standard', single_colorbar = False, interactive = True):
        self.interactive_ = interactive
        if interactive:
            from pylab import gcf
            self.figure_ = gcf()
        self.newFigure(1)
        self.layout_ = Layout(geometry = layout,scanmode = scanmode,single_colorbar = single_colorbar,figure = self.figure_)

    def newFigure(self,page):
        if self.interactive_:
            import matplotlib.pyplot as plt
            self.figure_ = plt.figure(page)
            return self.figure_
        else:
            self.figure_ = Figure()
            self.canvas_ = FigureCanvas(self.figure_)
        return self.figure_

    def __call__(self,*args,**kargs):
        actors = dict(
            geography   = [],
            contour     = [],
            fields      = [],
            colorbar    = [],
            arrays      = []
        )
        for actor in args:
            what = None
            try:
                what = getattr(actor,'identify')
                what = what()
            except AttributeError:
                if isinstance(actor,Field):
                    what = 'fields'
                elif isinstance(actor,ma.masked_array):
                    what = 'arrays'
            if not what:
                raise ValueError('Actor %s, type %s is not known' % (actor.__str__(),type(actor)))
            actors[what].append(actor)
        if len(actors['geography']) > 1:
            raise ValueError('Only one geography can be used within one plotter call')
        subplot = self.layout_(self)
        self.plot(actors,subplot,**kargs)

    def draw(self,filename = None):
        if self.interactive_:
            import matplotlib.pyplot as plt
            plt.show()
        else:
            self.canvas_.print_figure(filename)
