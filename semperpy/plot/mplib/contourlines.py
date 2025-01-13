import numpy as np
from semperpy.plot.mplib.contour import Contour

class ContourLines(Contour):

    def __call__(self,figure,axes,field,x,y):
        y = [ -xx for xx in y ]
        cs = axes.contour(x,y,list(field.values()),**self)
        return cs
