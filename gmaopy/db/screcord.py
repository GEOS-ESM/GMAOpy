from semperpy.directive.directive import Directive
from gmaopy.db.database import Database

class SCRecord(Directive):
    def __init__(self,*args,**kargs):
        super(SCRecord,self).__init__(*args,**kargs)
        self.checkLanguage()

Database.registerRecordType('score',SCRecord)
