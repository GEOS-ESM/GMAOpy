from .helpsystem import HelpSystem

class ASCIIFormatter(object):

    def __call__(self,text):
        return '\n'.join(text)

HelpSystem.register_formatter('ascii',ASCIIFormatter)
