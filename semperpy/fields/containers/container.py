from semperpy.core.decorators import *

class Container(object):

    def isLoaded(self,loaded = None):
        return True

    def unload(self):
        pass

    @abstractMethod
    def shape(self):
        pass

    @abstractMethod
    def __call__(self):
        pass

    @abstractMethod
    def sqrt(self):
        pass

