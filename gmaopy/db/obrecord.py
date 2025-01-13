from semperpy.directive.directive import Directive
from gmaopy.db.database import Database

class OBRecord(Directive):
    def __init__(self,*args,**kargs):
        super(OBRecord,self).__init__(*args,**kargs)
        self.checkLanguage()

Database.registerRecordType('obsstat',OBRecord)
