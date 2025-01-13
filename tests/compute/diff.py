from semperpy.core.tools import apply_type_deep
from gmaopy.storage.textreader import TextReader
from gmaopy.db.obrecord import OBRecord

class File(TextReader):

    def __init__(self,filename):
        self.lines_ = {}
        super(File,self).__init__(filename,OBRecord())
        
    def header(self,header):
        self.header_ = header

    def directive(self,directive):
        directive = apply_type_deep(str,directive)
        self.lines_['|'.join(list(directive.values()))] = directive


f1 = File('obsstat.ref')
f2 = File('obsstat.txt')

k1 = sorted(f1.lines_.keys())
k2 = sorted(f2.lines_.keys())
eq = k1 == k2
print('files are identical:',eq)
