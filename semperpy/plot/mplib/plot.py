try:
    from mpl_toolkits.basemap import Basemap
except:
    from matplotlib.toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from numpy import meshgrid
from semperpy.core.tools import mergedicts_keep

class Plot(object):

    def __init__ (self, grid, **kargs):
        defaults = {}
        ll_lon,ll_lat,ur_lon,ur_lat = grid.rectangle()
        defaults['llcrnrlon'] = ll_lon
        defaults['llcrnrlat'] = ll_lat
        defaults['urcrnrlon'] = ur_lon
        defaults['urcrnrlat'] = ur_lat
        defaults['resolution'] = 'c'
        defaults['projection'] = 'cyl'
        defaults['lon_0'] = -180
        kargs = mergedicts_keep(kargs,defaults)

        self.map = Basemap(**kargs)

    def contourf(self,field,**kargs):
        m = self.map
        g = field.grid()
        x,y = m(*meshgrid(g.longitudes(),g.latitudes()))
        field = list(field.values()) - 273.
        cs = m.contourf(x,y,field,cmap=plt.cm.jet)
        plt.title('Claude is still trying')
        m.drawcoastlines()
        m.drawmapboundary()
        plt.show()

class _Plot(object):

    def __init__ (self, field, **kargs):
        defaults = {}
        ll_lon,ll_lat,ur_lon,ur_lat = field.grid().rectangle()
        defaults['llcrnrlon'] = ll_lon
        defaults['llcrnrlat'] = ll_lat
        defaults['urcrnrlon'] = ur_lon
        defaults['urcrnrlat'] = ur_lat
        defaults['resolution'] = 'c'
        #defaults['area_threshold'] = 10000.0
        defaults['projection'] = 'cyl'
        kargs = mergedicts_keep(kargs,defaults)

        self.field = field

        projection = kargs['projection']
        if projection == 'latlon' or projection == 'cyl':
            defaults['projection'] = 'cyl'
            self.labels = [1,0,0,1]
        elif projection=='geos':
            self.labels = [0,0,0,0]
            defaults['llcrnrlon'] = None
            defaults['llcrnrlat'] = None
            defaults['urcrnrlon'] = None
            defaults['urcrnrlat'] = None
            defaults['lon_0'] = -75.0 # subpoint longitude (GOES west)
            defaults['rsphere'] = (6378137.00,6356752.3142)
            defaults['satellite_height'] = 35785831.0
        elif projection=='orthogr' or projection=='ortho' or projection=='npo' or projection=='spo': 
            defaults['projection'] = 'ortho'
            self.labels = [0,0,0,0] 
            if projection=='npo':
                defaults['lon_0'] = -100.0
                defaults['lat_0'] = +90.0
            elif projection=='spo':
                defaults['lon_0'] = -50.0
                defaults['lat_0'] = -90.0
            elif ll_lat >= 0:
                defaults['lon_0'] = -100.0
                defaults['lat_0'] = +90.0
            else:
                defaults['lon_0'] = -90.0
                defaults['lat_0'] = +45.0
        elif projection=='stereo' or projection=='stere' or projection=='nps' or projection=='sps':
            defaults['projection'] = 'stereo'
            self.labels = [0,0,0,0]
            if proj=='nps':
                defaults['lon_0'] = -90.0
                defaults['lat_0'] = +20.0
            elif proj=='sps':
                defaults['lon_0'] = -50.0
                defaults['lat_0'] = -20.0
            elif ll_lat >= 0:
                defaults['lon_0'] = -90.0
                defaults['lat_0'] = +20.0
            else:
                defaults['lon_0'] = -50.0
                defaults['lat_0'] = -20.0
            if defaults['lat_0'] > 0:
                defaults['projection'] = 'npstere'
            else:
                defaults['projection'] = 'spstere'
        else:
            self.labels = [0,0,0,0]

        kargs = mergedicts_keep(kargs,defaults)
        self.projection = kargs['projection']
        self.map = Basemap(**kargs)

    def contourf (self,**kwopts):
        """
        Wrapper around Basemap.contourf() with axis, colorbar and map
        transformations based on the current dimension environment/
        map projection.
        """
        self._contourf(**kwopts)

    def contour(self,**kwopts):
        """
        Wrapper around Basemap.contour() with axis, colorbar and map
        transformations based on the current dimension environment/
        map projection.
        """
        self._contourf(cfill=False,clines=True,**kwopts)

#   ..................................................................

    def _contourf ( self, bgim=None, 
                    N=None, V=None, cfill=True, clines=False, 
                    mpcol=None, sub=None, dlat=None, dlon=None,
                    Nx=None, Ny=None, Map=True,
                    **kwopts):
        
        m = self.map

#       Evaluate GrADS expression
#       -------------------------
        Z = list(self.field.values())[0,0]
        g = self.field.grid()

#       Setup axis
#       ----------
        fig = gcf()
        if sub==None:
            if cfill:
                ax = fig.add_axes([0.1,0.1,0.75,0.75])
            else:
                ax = fig.add_axes([0.1,0.1,0.8,0.8])
        else:
            ax = fig.add_subplot(sub)

#       Display the contour map
#       -----------------------
        X,Y = m(*meshgrid(g.longitudes(),g.latitudes()))
        if bgim != None:
            col = 'y'
            m.imshow(bgim)  # background image like a Sat Image
        else:
            col = 'k'
        if mpcol == None:  mpcol=col
        if V==None:
            if N==None: N=16
            if clines and cfill:
                cs = m.contour(X,Y,Z,N,linewidths=0.5,colors='k')
            elif clines:
                cs = m.contour(X,Y,Z,N,linewidths=1.25)
                cs.clabel(fmt='%1.0f') 
            if cfill:
                cs = m.contourf(X,Y,Z,N,**kwopts)
        else:
            if clines and cfill:
                cs = m.contour(X,Y,Z,V,linewidths=0.5,colors='k')
            elif clines:
                cs = m.contour(X,Y,Z,V,linewidths=1.25)
                cs.clabel(fmt='%1.0f') 
            if cfill:
                cs = m.contourf(X,Y,Z,V,**kwopts)
            
#       Color Bar
#       ---------
        if cfill:
            bbox = ax.get_position()
            if type(bbox) is ListType:
                l,b,w,h = bbox        # older mpl < 0.98
            else:
                l,b,w,h = bbox.bounds # mpl >= 0.98
            cax = axes([l+w+0.02, b, 0.04, h]) # setup colorbar axes.
            colorbar(drawedges=True,cax=cax) # draw colorbar
            axes(ax)  # make the original axes current again

#       Continents
#       ----------
        m.drawcoastlines(color=mpcol)
        m.drawmapboundary()
