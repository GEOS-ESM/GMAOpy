from gmaopy.db.database import Database
from gmaopy.storage.reader import Reader

class DBReader(Database):

    cache_ = {}

    def __new__(cls,db_name):
        if db_name in cls.cache_:
            return cls.cache_[db_name]
        return super(DBReader,cls).__new__(cls)

    def __init__(self,db_name):
        super(DBReader,self).__init__(db_name, overwrite = False)
        self.generic_ = self.getRecordType()()

    def __del__(self):
        self.close()

    def __call__(self,directive,columns,order_by=[]):
        if self.generic_ is not None:
            new = dict()
            for k,i in list(directive.items()):
                if k in self.generic_:
                    new[k] = i
        return super(DBReader,self).retrieve(new,columns,order_by,directive.negated())

Reader.register('dbreader',DBReader)
