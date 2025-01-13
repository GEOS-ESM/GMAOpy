from gmaopy.db.database import Database

class DBQuery(Database):

    cache_ = {}

    def __new__(cls,db_name):
        if db_name in cls.cache_:
            return cls.cache_[db_name]
        return super(DBQuery,cls).__new__(cls,db_name)

    def __init__(self,db_name):
        super(DBQuery,self).__init__(db_name, overwrite = False)
        self.generic_ = self.getRecordType()()

    def __del__(self):
        self.close()

    def __call__(self,query,directive = {}):
        new = directive
        if self.generic_ is not None:
            new = dict()
            for k,i in list(directive.items()):
                if k in self.generic_:
                    new[k] = i
        q = 'select %s from %s.v_view' % (query,self.prefix_)
        if len(directive) > 0:
            q = 'select %s from %s.v_view where %s;' % (query,self.prefix_,self.driver_.select_statement(directive,list(directive.keys()),{}))
        return self.query(q)
