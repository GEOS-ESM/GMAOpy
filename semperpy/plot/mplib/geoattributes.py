import numpy as np
from semperpy.plot.mplib.graphdirective import GraphDirective

class Coastlines(GraphDirective):
    def __call__(self,layout,subplot,basemap,geography):
        basemap.drawcoastlines(ax = subplot, **self)
coastlines = Coastlines

class Continents(GraphDirective):
    def __call__(self,layout,subplot,basemap,geography):
        basemap.fillcontinents(ax = subplot, **self)
continents = Continents

class Boundary(GraphDirective):
    def __call__(self,layout,subplot,basemap,geography):
        basemap.drawmapboundary(ax = subplot, **self)
boundary = Boundary

class Countries(GraphDirective):
    def __call__(self,layout,subplot,basemap,geography):
        basemap.drawcountries(ax = subplot, **self)
countries = Countries

class States(GraphDirective):
    def __call__(self,layout,subplot,basemap,geography):
        basemap.drawstates(ax = subplot, **self)
states = States

class Rivers(GraphDirective):
    def __call__(self,layout,subplot,basemap,geography):
        basemap.drawrivers(ax = subplot, **self)
rivers = Rivers

class ColorBar(GraphDirective):  
    pass

class Parallels(GraphDirective):
    def __call__(self,layout,subplot,basemap,geography):
        basemap.drawparallels(np.arange(geography['south'],geography['north']+1.,self['increment'])[1:-1],ax = subplot, **self.make_kwargs())
parallels = Parallels
    
class Meridians(GraphDirective):
    def __call__(self,layout,subplot,basemap,geography):
        basemap.drawmeridians(np.arange(geography['west'],geography['east'],self['increment']),ax = subplot, **self.make_kwargs())
meridians = Meridians
