import semperpy.core.exceptions as ex

class __Decorator__(object):
    def __init__(self,f):
        self.f_ = f

class abstractMethod(__Decorator__):
    def __call__(self,*args,**kwargs):
        raise ex.AbstractMethod("Method %s is abstract, the subclass should implement it" % self.f_)
