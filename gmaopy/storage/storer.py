from semperpy.core.factory import Factory
from gmaopy.storage.storage import Storage

class Storer(Storage):
    factory_ = Factory()

class StorerCollection(object):

    def __init__(self,storers,**kargs):
        self.storers_ = []
        for storer in storers:
            self.storers_.append(Storer.create(storer,**kargs))

    def __call__(self,*args,**kargs):
        for s in self.storers_:
            s(*args,**kargs)

    def flush(self,*args,**kargs):
        for s in self.storers_:
            s.flush(*args,**kargs)
