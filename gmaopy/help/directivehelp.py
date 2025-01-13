from semperpy.directive.asciiformatter import ASCIIFormatter
from semperpy.directive.help import Help
from .helpsystem import HelpSystem
from .nullformatter import NullFormatter
from gmaopy.modules.help import *

class DirectiveHelp(object):
    
    def __init__(self,format,*args):
        self.format_ = format
        self.name_ = None
        if len(args) > 0:
            self.name_ = args[0]

    def __call__(self):
        h = Help()
        return h(self.name_,self.format_)


HelpSystem.register_module('directives',DirectiveHelp)
HelpSystem.register_formatter('ascii',NullFormatter,'directives')
