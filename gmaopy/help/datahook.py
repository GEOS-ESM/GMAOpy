from gmaopy.hooks.datahook import DataHook
from gmaopy.help.helpsystem import HelpSystem

class Hook(object):
    
    def __init__(self,format,*args):
        self.format_ = format
        self.name_ = None
        if len(args) > 0:
            self.name_ = args[0]

    def __call__(self):
        if self.name_ is None:
            return DataHook.hookList()
        else:
            h = DataHook.hook(self.name_)
            return h.usage()

HelpSystem.register_module('datahook',Hook)
