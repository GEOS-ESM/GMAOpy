import os
from semperpy.core.date import Date
from gmaopy.help.helpsystem import HelpSystem

class Config(object):
    
    def __init__(self,format,*args):
        pass

    def __call__(self):
        empty = [' ']
        title = ['Configuration path(s):'] + empty
        text = [os.environ['SEMPERPY_CONFIG']]
        d = Date()
        tail = empty + ['generated on %s' % d] + empty
        return title + text + tail


HelpSystem.register_module('config',Config)
