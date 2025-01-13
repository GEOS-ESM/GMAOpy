import copy
from mpl_toolkits.basemap import Basemap
from semperpy.plot.mplib.graphdirective import GraphDirective

class Geography(GraphDirective):

    def __init__(self,*args,**kwargs):
        super(Geography,self).__init__(*args,**kwargs)
        self.basemap_ = None

    def get_basemap(self):
        return self.basemap_
    def set_basemap(self,new):
        self.basemap_ = new
    basemap = property(get_basemap,set_basemap)

    def createBasemap(self,layout,subplot):
        return Basemap(ax = subplot,**self.make_kwargs())

    def __call__(self,layout,subplot,where):
        if self.basemap_ is None:
            self.basemap_ = self.createBasemap(layout,subplot)
        for item in self['plot_' + where]:
            i = copy.copy(self[item])
            order = i['zorder']
            if order is None:
                order = 1
            if where == 'over':
                i['zorder'] = self['zorder'] + order
            elif order > self['zorder']:
                i['zorder'] = order - self['zorder']
            i(layout,subplot,self.basemap,self)

    def setLabels(self,*labels):
        self['parallels']['labels'] = labels
        self['meridians']['labels'] = labels
    
    def setIfMissing(self,name,value):
        if not name in self:
            self[name] = value

    def setGrid(self,ll_lat,ll_lon,ur_lat,ur_lon):
        self.setIfMissing('south',ll_lat)
        self.setIfMissing('west',ll_lon)
        self.setIfMissing('north',ur_lat)
        self.setIfMissing('east',ur_lon)
        self.setLabels(1,0,0,1)
        if self['projection'] == 'cyl': 
            self['llcrnrlon'] = self['west']
            self['llcrnrlat'] = self['south']
            self['urcrnrlon'] = self['east']
            self['urcrnrlat'] = self['north']
            self.setLabels(1,0,0,1)
            del(self['satellite_height'])
            del(self['rsphere'])
        elif self['projection'] == 'geos':
            self['llcrnrlon'] = None
            self['llcrnrlat'] = None
            self['urcrnrlon'] = None
            self['urcrnrlat'] = None
            self.setIfMissing('lon_0',-75.0)
            self.setLabels(0,0,0,0)
        elif self['projection'] == 'ortho':
            defaults = {}
            if not 'hemisphere' in self:
                if self['south'] >= 0:
                    self.setIfMissing('lon_0',100.0)
                    self.setIfMissing('lat_0',90.0)
                else:
                    self.setIfMissing('lon_0',-90.0)
                    self.setIfMissing('lat_0',-45.0)
            else:
                if self['hemisphere'] == 'north':
                    self.setIfMissing('lon_0',-100.0)
                    self.setIfMissing('lat_0',90.0)
                elif self['hemisphere'] == 'south':
                    self.setIfMissing('lon_0',-50.0)
                    self.setIfMissing('lat_0',-90.0)
            self.setLabels(0,0,0,0)
            del(self['satellite_height'])
            del(self['rsphere'])
        elif self['projection'] == 'stere':
            if not 'hemisphere' in self:
                if self['south'] >= 0:
                    self.setIfMissing('lon_0',-90.0)
                    self.setIfMissing('lat_0',self['south'])
                    self.setIfMissing('lat_ts',self['lat_0'])
                else:
                    self.setIfMissing('lon_0',-50.0)
                    self.setIfMissing('lat_0',self['north'])
                    self.setIfMissing('lat_ts',self['lat_0'])
            else:
                if self['hemisphere'] == 'north':
                    self.setIfMissing('lon_0',-90.0)
                    self.setIfMissing('lat_0',self['south'])
                    self['projection'] = 'npstere'
                elif self['hemisphere'] == 'south':
                    self.setIfMissing('lon_0',-50.0)
                    self.setIfMissing('lat_0',self['north'])
                    self['projection'] = 'spstere'
            self['llcrnrlon'] = self['west']
            self['llcrnrlat'] = self['south']
            self['urcrnrlon'] = self['east']
            self['urcrnrlat'] = self['north']
            self['boundinglat'] = self['lat_0']
            self.setLabels(0,0,0,0)

    def __copy__(self):
        new = super(Geography,self).__copy__()
        for attr in ['basemap_']:
            try:
                setattr(new,attr,getattr(self,attr))
            except AttributeError:
                pass
        return new

geography = Geography
