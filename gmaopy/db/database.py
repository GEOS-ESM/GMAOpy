from semperpy.core.tools import to_list
from semperpy.core.configfile import ConfigFile
from semperpy.core.configure import Configure
import semperpy.db.database

class Database(semperpy.db.database.Database):

    recordtypes_ = {}

    def __init__(self,db_name,write=False,overwrite = False, buffer = 2000):
        config = Configure('semperpy')
        loc = config.localise()
        db = config.file('databases%s.def' % loc,'config','db')
        databases = ConfigFile(db)
        if not db_name in databases:
            raise SystemError('The database "%s" is unknown' % db_name)
        db = databases[db_name] 
        schema = db['schema']
        if 'buffer' in db:
            buffer = int(db['buffer'])
        self.recordtype_ = db['recordtype']
        if not self.recordtype_ in self.recordtypes_:
            raise IndexError('Unknown record type "%s", known types: %s' % (self.recordtype_,', '.join(self.recordtypes_)))
        file = config.file(schema,'config','db')
        if len(file) > 1:
            raise SystemError('more than one schema definition file were found: %s' % (','.join(file)))
        if write:
            userlist = to_list(db['userw'])
        else:
            userlist = to_list(db['userr'])
        del(db['userr'])
        del(db['userw'])
        if 'password' in db and write:
            del(db['password'])
        done = False
        while not done:
            db['user'] = userlist[0]
            userlist.pop(0)
            try:
                super(Database,self).__init__(db_name,db,ConfigFile(file[0]),overwrite=overwrite,buffer_size=buffer,write=write)
                done = True
            except:
                if len(userlist) == 0:
                    raise

    def getRecordType(self):
        return self.recordtypes_[self.recordtype_]

    @classmethod
    def getNamedRecordType(self,name):
        if not name in self.recordtypes_:
            raise IndexError('Unknown record type "%s", known types: %s' % (name,', '.join(self.recordtypes_)))
        return self.recordtypes_[name]

    @classmethod
    def registerRecordType(self,name,_type):
        self.recordtypes_[name] = _type

    @classmethod
    def dbInfo(self,db_name):
        config = Configure('semperpy')
        loc = config.localise()
        db = config.file('databases%s.def' % loc,'config','db')
        databases = ConfigFile(db)
        if not db_name in databases:
            raise SystemError('The database "%s" is unknown' % db_name)
        return databases[db_name]

    @classmethod
    def createDBGenericRecord(self,name):
        if not name in self.recordtypes_:
            raise IndexError('Unknown record type "%s", known types: %s' % (recordtype,', '.join(self.recordtypes_)))
        return self.recordtypes_[name]()
