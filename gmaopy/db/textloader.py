from semperpy.directive.directive import Directive
from gmaopy.db.dbloader import DBLoader

class TextLoader(Directive):

    def __init__(self,*args,**kargs):
        super(TextLoader,self).__init__(*args,**kargs)
        self.checkLanguage()
        loader = DBLoader(self['files'],self['database'],overwrite=self['overwrite'],check_domains=self['check_domains'],dry_run=self['dry_run'])

textloader = TextLoader
