from semperpy.plot.mplib.plotattributes import ColorBar

class Contour(dict):

    def __init__(self,**kargs):
        for key,item in list(kargs.items()):
            self[key] = item
        if not 'colorbar' in self:
            self['colorbar'] = ColorBar()

    def identify(self):
        return 'contour'
