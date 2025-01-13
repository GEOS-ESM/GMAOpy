from semperpy.plot.mplib.plotter import Plotter
from numpy import meshgrid
try:
    from mpl_toolkits.basemap import Basemap
except:
    from matplotlib.toolkits.basemap import Basemap
from semperpy.fields.field import Field

class GeoPlotter(Plotter):

    def plot(self,actors,subplot):
        grid = actors['fields'][0].grid()
        actors['geography'][0].setGrid(grid)
        basemap = Basemap(ax = subplot,**actors['geography'][0].basemap())
        x,y = basemap(*meshgrid(grid.longitudes(),grid.latitudes()))
        # calling the object for drawing
        actors['geography'][0](True,subplot,x,y,basemap,grid,actors['fields'])
        contours = []
        for i in range(len(actors['contour'])):
            contours.append(actors['contour'][i](self.figure_,subplot,x,y,basemap,actors['fields'][i]))
        actors['geography'][0](False,subplot,x,y,basemap,grid,actors['fields'])
