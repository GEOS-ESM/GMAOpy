from gmaopy.db.database import Database
from gmaopy.storage.storer import Storer

class DBStorer(Database):

    def __init__(self,database, overwrite = False, buffer = 2000,**kargs):
        if buffer is None:
            self.store_method_ = self.call
        else:
            self.store_method_ = self.call_buffered
        super(DBStorer,self).__init__(database,overwrite=overwrite,buffer=buffer,write = True)

    def __del__(self):
        self.close()

    def call(self,directive):
        self.store(directive)

    def call_buffered(self,directive):
        self.store_buffered(directive)

    def __call__(self,*args,**kargs):
        self.store_method_(*args,**kargs)

Storer.register('dbstorer',DBStorer)
