from semperpy.core.tools import classname
from semperpy.core.factory import Factory

class Score(object):

    factory_ = Factory()
    domains_ = None

    @classmethod
    def register(self,name,klass):
        self.factory_.register(name,klass)

    @classmethod
    def knownScores(self):
        return set(self.factory_.keys())

    @classmethod
    def create(self,name,*args,**kargs):
        return self.factory_.create(name,*args,**kargs)

    def name(self):
        return classname(self)

    def preprocess(self,pool):
        pass

def ValidateScores(directive,keyword,values,*args):
    unknown = []
    known = Score.knownScores()
    for value in values:
        if not value in known: 
            unknown.append(value)
    if len(unknown) > 0:
        raise ValueError('Unknown score(s):\n%s' % ('\n'.join(unknown)))
    return values
