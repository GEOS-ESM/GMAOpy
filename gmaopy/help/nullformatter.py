from .helpsystem import HelpSystem

class NullFormatter(object):

    def __call__(self,text):
        return text
