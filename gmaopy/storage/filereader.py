import re
from semperpy.core.index import Index
from gmaopy.storage.reader import Reader
from gmaopy.storage.textreader import TextReader

class FileReader(TextReader):

    index_ = None

    def header(self,header):
        if self.index_ is None:
            FileReader.index_ = Index(*header,unique_keys = True)

    def directive(self,directive):
        self.index_.insert(directive,**directive)

    def __str__(self):
        return self.index_.__str__()

    def __call__(self,directive,columns,order_by = []):
        result = []
        values = self.index_.access(**directive)
        for value in values:
            cols = []
            for key in columns:
                cols.append(value[key])
            result.append(cols)
        return result

Reader.register('filereader',FileReader)
