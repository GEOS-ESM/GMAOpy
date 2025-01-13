import math
import numpy as np
import numpy.ma as ma
from semperpy.core.decorators import abstractMethod
from gmaopy.stats.critval import critval
from gmaopy.stats.statistics import Statistics

class Identical(Statistics):

    def transform(self,value):
        return value

    def transform_back(self,value):
        return value

    def compute_db(self,columns,data,variable):
        v = self.data2np(data,columns['value'])
        if len(v) == 0:
            return self.array(self.missing_value)
        v,ignore = self.mean(v)
        return self.array(v)

    def significance(self,reference, exp, lev=0.9): # ref and exp are backwards from diffplot!
        diff = self.difference(reference,exp)
        v = self.transform(diff)
        n = ma.count(v,0)
        v = v - np.mean(v,0)
        w = (np.sum(v * v,0)) / (n - 1)
        critvals = np.zeros(n.shape[0])
        for i in range(len(n)):
            critvals[i] = critval(lev,n[i])
        dx = critvals * np.sqrt(w / n)
        upper = self.transform_back(dx)
        lower = -upper
        diff = self.transform_back(diff)
        return diff,lower,upper

    def difference(self,reference,exp):
        return reference - exp

class RootMeanSquare(Identical):
    
    def name():
        return 'rms'

    def mean(self,value):
        #v = value * value
        m = np.mean(value, 0)
        #m = np.sqrt(m)
        count = ma.count(value,0)
        if isinstance(count,np.ndarray):
            if not count.shape: return m,0
            count = count[0]
        return m,count

class Correlation(Identical):
    
    def name():
        return 'cor'

    def transform(self,value):
        return 0.5 * np.log((1.0 + value) / (1.0 - value + 5.0e-6))

    def transform_back(self,value):
        return (np.exp(2 * value) - 1) / (np.exp(2 * value) + 1)

    def mean(self,value):
        null = value == 0
        if not np.any(null):
            transform = self.transform(value)
            m = np.mean(transform,0)
            m = self.transform_back(m)
        else:
            m = np.mean(value,0)
        count = ma.count(value,0)
        if isinstance(count,np.ndarray):
            if not count.shape: return m,0
            count = count[0]
        return m,count

    def significance1(self,value):
        v = self.transform(value)
        n = ma.count(v,0)
        v1 = np.sum(v * v,0)
        v2 = np.mean(v,0)
        w = (v1 - n * v2 * v2) / (n - 1)
        critvals = np.zeros(n.shape[0])
        for i in range(len(n)):
            critvals[i] = critval(0.90,n[i])
        dx = critvals * np.sqrt(w / n)
        upper = self.transform_back(dx)
        lower = self.transform_back(-dx)
        return lower,upper

#-------------------------------------------------------------
# Here we register our statistic classes under the name
# they are known by the user.
#-------------------------------------------------------------
Statistics.register('score','rms',RootMeanSquare)
Statistics.register('score','rms_bar',RootMeanSquare)
Statistics.register('score','rms_dis',RootMeanSquare)
Statistics.register('score','rms_dsp',RootMeanSquare)
Statistics.register('score','rms_ran',RootMeanSquare)
Statistics.register('score','cor',Correlation)
