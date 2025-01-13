from gmaopy.storage.storer import Storer

class NullStorer(object):

    def __init__(self,database,overwrite = False,debug = False,**kargs):
        pass

    def __call__(self,directives):
        pass

    def flush(self):
        pass

Storer.register('nullstorer',NullStorer)
