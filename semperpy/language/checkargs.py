from semperpy.language.language import Language

class checkArgs(object):
    
    reg_ = {}

    @classmethod
    def register(self,name,what):
        self.reg_[name] = what

    def __init__(self,func):
        self.f_ = func

    def __call__(self,*args,**kargs):
        kargs = Language.resolveDirective(kargs,self.f_.__name__,self.reader())
        self.f_(self,*args,**kargs)


    def reader(self):
        class Reader(object):
            def __init__(self,me):
                self.owner_ = me
            def __call__(self,name):
                return self.owner_.reg_[name]
        return Reader(self)
