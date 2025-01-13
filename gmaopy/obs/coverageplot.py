import copy
import numpy as np
from mpl_toolkits.basemap import Basemap
from semperpy.language.validate import languageValidation
from semperpy.core.tools import to_list
from semperpy.fields.grid import Grid
from semperpy.geo.domain import Domain
from gmaopy.obs.odscolorbarplot import ODSColorbarPlot

class CoveragePlot(ODSColorbarPlot):

    domaindef_ = Domain.domains('SEMPERPY')

    def checkLanguage(self,*args,**kwargs):
        if 'plotdata' in self:
            data = self.data
            if 'variable' in data:
                v = set(to_list(data['variable']))
                # the user defined a variable to plot on top of lat and lon
                if len(v) == 1:
                    data['variable'] = ['lat','lon',v.pop()]
                else: 
                    if not 'lat' in v or not 'lon' in v and not len(v) == 3:
                        raise ValueError('The keyword "variable" can only contain the name of a variable from the ODS file, (e.g. omf, obs, oma)')
            else:
                data['variable'] = ['lat','lon']
        super(CoveragePlot,self).checkLanguage(*args,**kwargs)

    def draw(self,layout,subplot):
        self.dispatchGraphicsAttributes('sym')
        count = 0
        for curve in self.curves_:
            geo = copy.copy(self['geography'])
            geo.setGrid(*self.domaindef_[curve.data['domain_name']].coordinates_sn())
            lat = curve.data.variables(variable = 'lat')
            lon = curve.data.variables(variable = 'lon')
            var = None
            if len(curve.data['variable']) > 2:
                var = curve.data.variables(variable = curve.data['variable'][-1])
            count += lat.shape[0]
            geo(layout,subplot,'below')
            if not lon.any():
                lon = [0]
                lat = [0]
                curve['symbol']['s'] = 0
            try:
                x,y = geo.basemap(lon,lat)
                if len(x) == len(y):
                    if var is None:
                        if type(curve['graphics']['color']) is list:
                            o = geo.basemap.scatter(x,y,c=curve['graphics']['color'][0],**curve['symbol'])
                        else:
                            symdict = { k:v for k,v in curve['symbol'].items() if k != 'faceted'}
                          # o = geo.basemap.scatter(x,y,c=curve['graphics']['color'],**curve['symbol'])
                            o = geo.basemap.scatter(x,y,c=curve['graphics']['color'],**symdict)
                        curve['_graph_'] = o
                    else:
                        self.setColorMap(layout,subplot,var)
                        cm = self['colormap']
                        o = geo.basemap.scatter(x,y,c=var,cmap=cm.cmap_,vmin=cm['min'],vmax=cm['max'],**curve['symbol'])
                        curve['_graph_'] = o
                        self.drawColorbar(layout,subplot)
            except Exception as e:
                print(e)
                print('failed')
            geo(layout,subplot,'over')
        self['obscount'] = count

coverageplot = CoveragePlot
