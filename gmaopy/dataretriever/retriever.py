import copy
import re
from semperpy.core.tools import substitute_variables
from semperpy.core.innerpython import InnerPython
from semperpy.core.configfile import ConfigFile
from semperpy.core.configure import Configure

class Retriever(object):

    config_ = None

    def configuration(self):
        if self.config_ == None:
            Retriever.config_ = ConfigFile(Configure.path('MAIN_CONFIG','gmao') + '/retrieve.def')
        return self.config_

    def url(self,directive,kind,which,media):
        config = self.configuration()
        source = directive['source']
        url = config[kind][source]
        url = substitute_variables(url,directive)
        if config['build_url'][source] == 'yes':
            type = directive['type'] + '_' + media
            url += '/' + substitute_variables(config[which][type],directive)
        return url

    def findReader(self,source):
        config = self.configuration()
        return InnerPython.get_class(config[source]['reader'])
