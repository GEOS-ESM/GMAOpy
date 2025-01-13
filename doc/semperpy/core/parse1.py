from semperpy.core.truthparser import TruthParser

class MyParser(object):

    def compile(self,expression):
        parser = TruthParser()
        return parser.parse(expression,self)

p = MyParser()
print(p.compile('2 < 4 and (9 < 1 or 2 == 2'))
# returns True
