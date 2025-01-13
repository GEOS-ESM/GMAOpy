import re
from semperpy.core.index import Index

class ScoreFileReader(object):

    types_ = dict(
        level = float,
        date = int,
        step = int,
        value = float
    )

    def __init__(self,filename):
        self.file_ = None
        self.scores_ = None
        self.file_ = open(filename,'r')

    def __del__(self):
        self.close()

    def close(self):
        if self.file_:
            self.file_.close()
            self.file_ = None

    def read(self):
        lines = [ re.sub('\n','',x) for x in self.file_.readlines() ]
        keys = lines[0].split('|')
        columns = list(range(len(keys)))
        indexkeys = list(keys)
        value = indexkeys.index('value')
        del(indexkeys[value])
        self.scores_ = Index(*indexkeys)
        for i in range(1,len(lines)):
            values = lines[i].split('|')
            item = {}
            for j in columns:
                value = values[j]
                if keys[j] in self.types_:
                    value = self.types_[keys[j]](value)
                item[keys[j]] = value
            self.scores_.insert(item['value'],**item)
        return self.scores_

    def scores(self):
        return self.scores_
