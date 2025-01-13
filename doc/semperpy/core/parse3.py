import numpy as np
from semperpy.core.truthparser import TruthParser

class MyParser(object):

    def __init__(self):
        self.arrays_ = dict(
            x = np.arange(100),
            y = np.arange(99,-1,-1),
            z = np.random.rand(100) * 100,
        )

    def createVariable(self,what):
        return TruthParser.Value(self.arrays_[what])

    def createLogical(self,what):
        if what == 'and':
            return np.logical_and
        else:
            return np.logical_or

    def compile(self,expression):
        parser = TruthParser()
        return parser.parse(expression,self)

    def extract(self,mask):
        return self.arrays_['z'][mask]

p = MyParser()
mask = p.compile('x == 49 and y == 50')
print(mask)
mask = p.compile('x < y')
print(mask)
value = p.extract(mask)
print(value.shape)
print(value)
