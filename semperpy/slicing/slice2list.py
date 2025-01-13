#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, February 2011, claude.gibert@synopticview.com
#-------------------------------------------------------------------
from semperpy.core.tools import distribute

class Slice2List(object):

    def __init__(self,visitor):
        self.visitor_ = visitor

    def __call__(self,dimensions,variable,src,dst,meta,is_interval,**kargs):
        s1 = self.sliceShape(src)
        s2 = [ len(x) for x in meta ]
        if s1 != s2:
            ValueError('Discrepancy between metadata and slices')
        self.create(dimensions,variable,src,meta,is_interval,**kargs)

    def create(self,_dimension,variable,src,meta,is_interval,where = [],md = {},**kargs):
        if len(meta) == 0:
            self.visitor_(distribute(where),md,**kargs)
        else:
            md = dict(md)
            s = src[0]
            if not is_interval[0]:
                theslice = []
                m = []
                for i in range(s[0].start,s[0].stop):
                    theslice.append(slice(i,i+1,1))
                    m.append(meta[0][i-s[0].start])
                for i in range(len(theslice)):
                    md[_dimension[0]] = m[i]
                    self.create(_dimension[1:],variable,src[1:],meta[1:],is_interval[1:],where + [theslice[i]],md,**kargs)
            else:
                md[_dimension[0]] = meta[0]
                self.create(_dimension[1:],variable,src[1:],meta[1:],is_interval[1:],where + [s],md,**kargs)

    def sliceShape(self,slice):
        s = []
        for v in slice:
            l = 0
            for vv in v:
                l += vv.stop - vv.start
            s.append(l)
        return s

    def preProcess(self,dimensions,variable,shape,slices,metadata):
        self.visitor_.preProcess(dimensions,variable,shape,slices,metadata)

    def postProcess(self,dimensions,variable,shape,slices,metadata):
        self.visitor_.postProcess(dimensions,variable,shape,slices,metadata)

    def fieldSet(self):
        return self.visitor_.fieldSet()
