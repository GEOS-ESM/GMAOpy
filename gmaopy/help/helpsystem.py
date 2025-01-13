from collections import defaultdict
from semperpy.core.factory import Factory

class HelpSystem(object):

    modules_ = Factory()
    formatters_ = defaultdict(Factory)

    @classmethod
    def help(self,format,*args):
        if len(args) == 0:
            formatter = self.formatters_[format].create('')
            return formatter(self.moduleList())
        name = args[0]
        formatter = self.formatters_[format].create(name)
        module = self.modules_.create(name,format,*args[1:])
        return formatter(module())

    @classmethod
    def register_module(self,name,klass):
        self.modules_[name] = klass

    @classmethod
    def register_formatter(self,name,klass,command = None):
        if command is None:
            self.formatters_[name]['__default__'] = klass
        else:
            self.formatters_[name][command] = klass

    @classmethod
    def moduleList(self):
        l = ['   ' + x for x in list(self.modules_.keys()) ]
        l.sort()
        return l
