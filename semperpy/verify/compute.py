from semperpy.core.innerpython import InnerPython
from semperpy.core.index import Index
from semperpy.directive import Directive
from semperpy.verify.scores import *
from semperpy.verify.filestorer import FileStorer

class Compute(Directive):
    
    actors_ = ['forecast','reference','persistence']

    def myorder(self,a,b):
        ia = self.actors_.index(a)
        ib = self.actors_.index(b)
        return cmp(ia,ib)

    def __init__(self,*args,**kargs):
        super(Compute,self).__init__(*args,**kargs)
        self.checkLanguage(self)
        for todo in self['todo']:
            todo.scoreobj = [ Score.create(x) for x in todo['score'] ]
        requirements = self.requirements([ x.scoreobj for x in self['todo'] ])
        for actor in self.actors_:
            if not actor in requirements:
                self[actor] = None
            elif not actor in self:
                type = self['_' + actor + '_default_class']
                self[actor] = InnerPython.get_class(type)()
                self[actor].checkLanguage(self)
        requirements = list(requirements)
        requirements.sort(self.myorder)
        self.adjustValues(requirements)
        print(self)
        self.index_ = self.retrieveValues(requirements)
        self.compute(requirements,self.index_)

    def __del__(self):
        self.file_.write(']')
        self.file_.close()

    def adjustValues(self,all):
        self.storer_ = FileStorer(self['output_file'])
        for item in all:
            self[item].adjustValues(self)

    def requirements(self,scores):
        all = []
        for score in scores:
            for v in score:
                all += v.requirements()
        return set(all)

    def retrieveValues(self,all):
        fieldset = []
        for actor in all:
            fieldset += self[actor].retrieveData(*self['todo'])
        index = Index('type','parameter','date','step','level')
        print("required: %d fields." % (len(fieldset)))
        for f in fieldset:
            index.insert(f,**f.metadata())
        print(index)
        return index

    def compute(self,requirements,index):
        forecast = self['forecast']
        reference = self['reference']
        for todo in self['todo']:
            for parameter in todo['parameter']:
                for level in todo['level']:
                    for i in range(len(forecast['date'])):
                        pool = {}
                        date = forecast['date'][i]
                        step = forecast['step'][i]
                        id = dict(
                            parameter = parameter,
                            level = level,
                            type = forecast['type'],
                            date = date,
                            step = step
                        )
                        fc = index.constrained_access(**id)
                        pool['forecast'] = fc
                        ref= index.constrained_access(
                                    parameter = parameter,
                                    level = level,
                                    type = reference['type'],
                                    date = self['reference']['date'][i],
                                    step = self['reference']['step'][i],
                        )
                        pool['reference'] = ref
                        if 'persistence' in requirements:
                            persistence = self['persistence']
                            pf = index.constrained_access(
                                     parameter = parameter,
                                     level = level,
                                     type = persistence['type'],
                                     date = self['persistence']['date'][i],
                                     step = self['persistence']['step'][i],
                            )
                            pool['persistence'] = pf
                        pool['weights'] = self.createWeights(fc)
                        scores = todo.scoreobj
                        for score in scores:
                            score.preprocess(pool)
                            score.computeScore(pool,todo,forecast,self.storer_,**id)

    def createWeights(self,forecast):
        return forecast.grid().weights()
             

compute = Compute
