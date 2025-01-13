from semperpy.directive.directive import Directive
from gmaopy.db.database import Database

class PRRecord(Directive):
    def __init__(self,*args,**kargs):
        super(PRRecord,self).__init__(*args,**kargs)
        self.checkLanguage()

Database.registerRecordType('product',PRRecord)
