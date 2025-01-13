import numpy.ma as ma
from semperpy.slicing.arraygenerator import ArrayGenerator

class ODSStatistics(object):
    
    stats_ = {}

    @classmethod
    def register(self,name,what):
        self.stats_[name] = what

    @classmethod
    def create(self,name):
        return self.stats_[name]()

    @classmethod
    def list2array(self,l):
        gen = ArrayGenerator(masked = True) 
        a = gen.create((len(l)))
        for i in range(len(l)):
            a[i] = l[i]
        a = gen.postProcess(a)
        return a

    def array(self,value):
        gen = ArrayGenerator(masked = True) 
        a = gen.create((1))
        a[0] = value
        a = gen.postProcess(a)
        return a

class Concat(ODSStatistics):
    
    def __call__(self,variables):
        all = []
        for name,var in variables.items():
            all += var
            variables[name] = ma.concatenate(tuple(var))
        return ma.concatenate(tuple(all))

class Count(ODSStatistics):
    
    def __call__(self,variables):
        keys = list(variables.keys())
        return self.list2array([ x.shape[0] for x in variables[keys[0]] ])

class TotalCount(ODSStatistics):
    
    def __call__(self,variables):
        keys = list(variables.keys())
        v = self.list2array([ x.shape[0] for x in variables[keys[0]] ])
        return self.array(v.sum())


ODSStatistics.register('concat',Concat)
ODSStatistics.register('count',Count)
ODSStatistics.register('totalcount',TotalCount)
