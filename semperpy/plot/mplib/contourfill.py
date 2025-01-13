import numpy as np
import numpy.ma as ma
from semperpy.plot.mplib.contour import Contour

class ContourFill(Contour):

    def __call__(self,figure,axes,field,x,y):
        y = [ -xx for xx in y ]
        cs   = axes.contourf(x,y,field,**self)
        if self['colorbar']:
            figure.colorbar(cs,ax=axes,**self['colorbar'])
        return cs
