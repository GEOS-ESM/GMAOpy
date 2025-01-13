from semperpy.plot.mplib.plotter import Plotter
from semperpy.fields.field import Field

class SlicePlotter(Plotter):

    def plot(self,actors,subplot,**kargs):
        diff = len(actors['contour']) - len(actors['fields'])
        if diff > 0:
            for i in range(diff):
                actors['fields'].append(actors['fields'][0])
        for i in range(len(actors['contour'])):
            actors['contour'][i](self.figure_,subplot,actors['fields'][i],**kargs)
