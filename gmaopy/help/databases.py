from semperpy.core.tools import is_list
from semperpy.core.date import Date
from semperpy.core.configfile import ConfigFile
from semperpy.core.configure import Configure
from gmaopy.help.helpsystem import HelpSystem
from gmaopy.db.database import Database

class Databases(object):
    
    def __init__(self,format,*args):
        self.database_ = None
        if len(args) > 0:
            self.database_ = args[0]

    def __call__(self):
        config = Configure('semperpy')
        loc = config.localise()
        db = config.file('databases%s.def' % loc,'config','db')
        databases = ConfigFile(db)
        lines = []
        empty = [' ']
        d = Date()
        tail = empty + ['generated on %s' % d] + empty
        if self.database_ is None:
            keys = list(databases.keys())
            keys.sort()
            for key in keys:
                comment = databases[key].get('comment','')
                if is_list(comment):
                    comment = ', '.join(comment)
                lines.append('%-8s: type = %-8s writer = %-8s %s' % (key,databases[key]['recordtype'],databases[key]['userw'],comment))
            return empty + ['List of available databases:'] + empty + lines + empty + tail + empty
        else:
            if not self.database_ in databases:
                raise IndexError('Database %s is unknown' % self.database_)
            db = databases[self.database_]
            lines.append('%s:' % self.database_)
            dbkeys = list(db.keys())
            dbkeys.sort()
            for k in dbkeys:
                lines.append('%-10s = %s' % (k, str(db[k])))
            lines += empty
            record = Database.createDBGenericRecord(db['recordtype'])
            keys = list(record.keys())
            keys.sort()
            lines.append('Keywords for %s: %s' % (self.database_,', '.join(keys)))
            return empty + lines + empty + tail + empty


HelpSystem.register_module('databases',Databases)
