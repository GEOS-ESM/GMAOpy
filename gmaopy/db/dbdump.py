from semperpy.directive.directive import Directive
from gmaopy.db.dbreader import DBReader
from gmaopy.storage.filestorer import FileStorer

class DBDump(Directive):

    def __init__(self,*args,**kargs):
        super(DBDump,self).__init__(*args,**kargs)
        expver = self['expver']
        self.checkLanguage() # causes experiment names (and filename) to be lowercase
        db_name = self['database']
        reader = DBReader(db_name)
        generic = reader.getRecordType()()
        specific = set(['begindate','enddate','filename','database','append','order'])
        directive = Directive()
        for key,item in list(self.items()):
            if (key in generic or key in specific) and not self.isDefault(key):
                directive[key] = item
                if 'expver' in key:
                    directive[key] = expver
        if len(directive) == 0:
            print('dumping the whole database')
        elif 'begindate' in self or 'enddate' in self:
            if not 'enddate' in self or not 'begindate' in self:
                raise ValueError('When specifiying begindate and enddate, both need to be specified')
            directive['date'] = { self['begindate'] : self['enddate'] }
            print(directive)
        keys = list(generic.keys())
        data = reader(directive,keys,order_by = self['order'])
        directive = {}
        print('writing data into %s...' % self['filename'])
        append = self['append']
        storer = FileStorer(self['filename'],overwrite = True,append=append)
        for row in data:
            for i,column in enumerate(keys):
                directive[column] = row[i]
            storer(directive)
        print('done')

dbdump = DBDump
