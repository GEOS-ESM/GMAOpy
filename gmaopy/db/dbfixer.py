from gmaopy.db.dbloader import DBLoader
from gmaopy.db.database import Database
from gmaopy.db.obrecord import OBRecord

class DBFixer(DBLoader):

    def __init__(self,files,database,overwrite = False,process = None):
        self.process_ = self.nothing
        if process is not None:
            self.process_ = process
        super(DBFixer,self).__init__(files,database,overwrite=overwrite)

    def directive(self,directive):
        directive = self.process_(directive)
        if directive is not None:
            self.db_.store_buffered(directive)

    def nothing(self,directive):    
        return directive


    
