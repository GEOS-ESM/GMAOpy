from semperpy.core.truthparser import TruthParser

class MyParser(object):

    def createVariable(self,what):
        return TruthParser.Value(self.variables_[what])

    def compile(self,expression,**variables):
        self.variables_ = variables
        parser = TruthParser()
        return parser.parse(expression,self)

p = MyParser()
print(p.compile('z <= 4 and (x > 1 or y == 2)',x = 10.0, y = 20.0, z = 3.0)) # True
print(p.compile('z <= 4 and (x > 1 or y == 2)',x = 1.0, y = 2.0, z = 3.0))   # True
print(p.compile('z <= 4 and (x > 1 or y == 2)',x = 1.0, y = 2.0, z = 5.0))   # False
