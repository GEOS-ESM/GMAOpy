from math import sqrt
import numpy as np
from semperpy.verify.score import *
from semperpy.fields.domain import Domain

#--------------------------------------------------------------------------------
# Scores involving forecast and reference
#--------------------------------------------------------------------------------
class ForecastError(Score):
    def requirements(self):
        return ['forecast','reference']

    def calculateError(self,pool):
        if not 'fe' in pool:
            pool['fe'] = (pool['forecast'] - pool['reference']) * pool['weights']

    def calculateErrorSquare(self,pool):
        if not 'fe2' in pool:
            pool['fe2'] = pool['fe'] * (pool['forecast'] - pool['reference'])

#--------------------------------------------------------------------------------
# Scores involving persistence forecast and reference
#--------------------------------------------------------------------------------
class PersistenceError(Score):
    def requirements(self):
        return ['persistence','reference']

    def calculateError(self,pool):
        if not 'pe' in pool:
            pool['pe'] = (pool['persistence'] - pool['reference']) * pool['weights']

    def calculateErrorSquare(self,pool):
        if not 'pe2' in pool:
            pool['pe2'] = pool['pe'] * pool['pe']

#--------------------------------------------------------------------------------
# functions
#--------------------------------------------------------------------------------
def computeMean(field,domain,weights):
    value = field.extract_subdomain(domain)
    ww = field.extract_subdomain_array(weights,domain)
    w = np.sum(ww)
    if w == 0:
        return 0
    return np.sum(value) / w

def computeRMS(field,domain,weights):
    value = computeMean(field,domain,weights)
    return sqrt(value)

#--------------------------------------------------------------------------------
# Scores
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------
# root mean square error
#--------------------------------------------------------------------------
class rmsfe(ForecastError):
    def preprocess(self,pool):
        self.calculateError(pool)
        self.calculateErrorSquare(pool)

    def computeScore(self,pool,todo,forecast,storer,**kargs):
        domains = Domain.domains()
        for domain in todo['domain']:
            kargs['value'] = computeRMS(pool['fe2'],domains[domain],pool['weights'])
            kargs['domain'] = domain
            kargs['score'] = self.name()
            storer(kargs)


#--------------------------------------------------------------------------
# mean error
#--------------------------------------------------------------------------
class meanfe(ForecastError):
    def preprocess(self,pool):
        self.calculateError(pool)

    def computeScore(self,pool,todo,forecast,storer,**kargs):
        domains = Domain.domains()
        for domain in todo['domain']:
            kargs['value'] = computeMean(pool['fe'],domains[domain],pool['weights'])
            kargs['domain'] = domain
            kargs['score'] = self.name()
            storer(kargs)
        
#--------------------------------------------------------------------------
# standard deviation of the error
#--------------------------------------------------------------------------
class stdvfe(ForecastError):
    pass

#--------------------------------------------------------------------------
# root mean square of the persistence forecast error
#--------------------------------------------------------------------------
class rmspe(PersistenceError):
    def preprocess(self,pool):
        self.calculateError(pool)
        self.calculateErrorSquare(pool)

    def computeScore(self,pool,todo,forecast,storer,**kargs):
        domains = Domain.domains()
        for domain in todo['domain']:
            kargs['value'] = computeRMS(pool['fe2'],domains[domain],pool['weights'])
            kargs['domain'] = domain
            kargs['score'] = self.name()
            storer(kargs)

#--------------------------------------------------------------------------
# mean persistence forecast error
#--------------------------------------------------------------------------
class meanpe(PersistenceError):
    def preprocess(self,pool):
        self.calculateError(pool)

    def computeScore(self,pool,todo,forecast,storer,**kargs):
        domains = Domain.domains()
        for domain in todo['domain']:
            kargs['value'] = computeMean(pool['pe'],domains[domain],pool['weights'])
            kargs['domain'] = domain
            kargs['score'] = self.name()
            storer(kargs)

#--------------------------------------------------------------------------
# standard deviation of persistence forecast error
#--------------------------------------------------------------------------
class stdvpe(PersistenceError):
    pass


Score.register('rmsfe',rmsfe)
Score.register('meanfe',meanfe)
Score.register('stdvfe',stdvfe)
Score.register('rmspe',rmspe)
Score.register('meanpe',meanpe)
Score.register('stdvpe',stdvpe)
