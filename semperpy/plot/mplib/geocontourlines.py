import numpy as np
from semperpy.plot.mplib.contour import Contour

class GeoContourLines(Contour):

    def __call__(self,figure,axes,x,y,basemap,field):
        data = np.squeeze(list(field.values()))
        cs = basemap.contour(x,y,data,cmap=self.colours_)
        return cs
