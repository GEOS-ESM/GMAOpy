import math
from collections import defaultdict
import numpy as np
import numpy.ma as ma
from semperpy.core.decorators import abstractMethod
from semperpy.slicing.arraygenerator import ArrayGenerator

class Statistics(object):
    factory_ = defaultdict(dict)
    cache_ = defaultdict(dict)

    missing_value = 1.7E38

    @classmethod
    def register(self,category,name,what):
        self.factory_[category][name] = what

    @classmethod
    def create(self,category,name):
        # In order to speed up the process, statistics once 
        # instanciated are reused.
        if category in self.cache_ and name in self.cache_[category]:
            return self.cache_[category][name]
        if not category in self.factory_:
            raise IndexError('Unknown category: "%s", known: %s' % (category,', '.join(list(self.factory_.keys()))))
        if not name in self.factory_[category]:
            raise IndexError('Unknown statistic "%s" in category "%s", known: %s' % (name,category,', '.join(list(self.factory_[category].keys()))))
        new = self.factory_[category][name]()
        self.cache_[category][name] = new
        new.name_ = name
        return new

    def data2np(self,data,index):
        # created a numpy array from one column index
        # amongst all data
        a = np.zeros(len(data))
        a = [0] * len(data)
        i = 0
        j = 0
        while i < len(data):
            if data[i][index] != self.missing_value:
                a[j] = data[i][index]
                j += 1
            i += 1
        return np.array(a[0:j])

    def split(self,data,index):
        result = defaultdict(list)
        for value in data:
            result[value[index]].append(value)
        return result

    def store(self,storer,record,**kargs):
        for k,i in list(kargs.items()):
            record[k] = i
        storer(record)

    def array(self,value):
        gen = ArrayGenerator(masked = True) 
        a = gen.create((1))
        a[0] = value
        a = gen.postProcess(a)
        return a

    def list2array(self,l):
        gen = ArrayGenerator(masked = True) 
        a = gen.create((len(l)))
        for i in range(len(l)):
            a[i] = l[i]
        a = gen.postProcess(a)
        return a

    def requirements_raw(self):
        return ['var']

    def requirements_db(self):
        return self.name_

    def unit(self):
        return None

    # each statistic needs to tell whether its value is better when 
    # it is bigger (e.g. correlation or fraction of benefical obs.) or worse
    # to be able to orient the curves and colorbars properly.
    def moreIsBetter(self):
        return False

    def columns(self):
        return []

    def prepareProcessing(self,what):
        pass

    def completeProcessing(self,what):
        pass

    @abstractMethod
    def name(self):
        pass

    @abstractMethod
    def compute_raw(self,variables,name,storer,record):
        pass

    @abstractMethod
    def compute_db(self,columns,data,name):
        pass

def statisticList(flat = None):
    all = []
    for category in Statistics.factory_:
        for name,klass in list(Statistics.factory_[category].items()):
            instance = klass()
            try:
                getattr(instance,'compute_db')
                if flat is None:
                    all.append((category,name))
                else:
                    all.append('%s: %s' % (category,name))
            except AttributeError:
                pass 
    return all
