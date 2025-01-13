from semperpy.directive import Directive
from semperpy.core.tools import dictionary, no_list, is_list, to_list
from semperpy.core.configfile import ConfigFile
from semperpy.core.configure import Configure
from gmaopy.dataretriever.dapretriever import DAPRetriever
from gmaopy.dataretriever.fileretriever import FileRetriever

class Retrieve(Directive):

    config_ = None
    
    def __init__(self,*args,**kargs):
        super(Retrieve,self).__init__(*args,**kargs)
        self.checkLanguage(self)
        self.value_ = self.retrieve()

    def configFile(self):
        if self.config_ == None:
            Retrieve.config_ =  ConfigFile(Configure.path('MAIN_CONFIG','gmao') + '/locations.def')
            for k,item in list(Retrieve.config_['access'].items()):
                Retrieve.config_['access'][k] = to_list(item)
        return self.config_

    def values(self):
        return self.value_

    def return_fieldset(self):
        return True

    def use_intervals(self):
        return False

    def retrieve(self):
        all =  self.doRetrieve()
        return all

    def doRetrieve(self):
        obj = dict(
            file = FileRetriever,
            dap = DAPRetriever,
        )
        all = []
        for field in self['fields']:
            config = self.configFile()
            retrievers = [ obj[x](self.use_intervals()) for x in config['access'][field['source']]]
            for variable in self['variables']:
                fields = self.find(retrievers,dictionary(field,**variable))
                all += fields
        return all

    def find(self,retrievers,directive):
        for retriever in retrievers:
            try:
                fields = retriever.retrieve(directive,**self.cleanup(directive))
                return fields
            except IOError:
                pass
        raise ValueError("field %s was not found" % (str(directive)))

    def cleanup(self,directive):
        directive = dict(directive)
        delete = []
        for k in directive:
            if is_list(directive[k]):
                delete.append(k)
        for k in delete:    
            del(directive[k])
        return directive


retrieve = Retrieve
