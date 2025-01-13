#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2010
#
# Claude Gibert, June 2010, dev@synopticview.com
#----------------------------------------------------------------------------
from semperpy.core.spjson import JSon

class JSonFile(JSon):

    def __init__(self,path = None):
        self.path_ = path

    @classmethod
    def path(self,path,name):
        name = name + ".json"
        if path != '':
            name = path + '/' + name
        return name

    def __call__(self,name):
        if self.path_ is not None:
            filename = self.path(self.path_,name)
        else:
            filename = name
        f = open(filename,"r")
        try:
            s = self.decode(f)
        except Exception: 
            print(filename)
            raise
        f.close()
        return s
