from gmaopy.storage.textreader import TextReader
from gmaopy.db.database import Database

class DBLoader(TextReader):

    def __init__(self,files,database,overwrite=False,check_domains=True,dry_run=False,missing_value=None):
        self.db_ = Database(database,overwrite = overwrite,write=True)
        super(DBLoader,self).__init__(files,self.db_.getRecordType()(),check_domains,dry_run,missing_value)
        self.db_.flush()

    def directive(self,directive,count,totalcount):
        def progress(msg):
            print('%s, %02d' % (msg,int(100 * float(count) / float(totalcount))) + '%')
        self.db_.store_buffered(directive,progress)

    def header(self,directive):
        pass

    
