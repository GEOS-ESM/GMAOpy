from semperpy.plot.mplib.contour import Contour

class GeoContourFill(Contour):

    def __call__(self,figure,axes,x,y,basemap,field):
        data = list(field.values())
        cs = basemap.contourf(x,y,data,**self)
        if self['colorbar']:
            figure.colorbar(cs,ax=axes,**self['colorbar'])
        return cs
