import math
import numpy as np
from gmaopy.stats.statistics import Statistics

class Sum(Statistics):
    """ 
        Computes the sum of values, both from raw files
        and from the database
    """

    def compute_raw(self,variables,name,storer,record):
        variable = variables[name]
        #print('Commonstats sum compute raw',str(np.sum(variable)), variable)
        self.store(storer,record,value=np.sum(variable),count=variable.shape[0])


    def compute_db(self,columns,data,name):
        v = self.data2np(data[name],columns['value'])
        if len(v) == 0:
            return self.array(self.missing_value)
        return self.array(np.sum(v))

    def name(self):
        return 'sum'

class Mean(Sum):
    """ 
        Computes the mean of values using the sum
        obtained from the database.
    """

    def compute_db(self,columns,data,name):
        value = self.data2np(data[name],columns['value'])
        count = self.data2np(data[name],columns['count'])
        if len(count) == 0:
            return self.array(self.missing_value)
        value = np.sum(value)
        count = np.sum(count)
        result = self.array(value / count)
        return result

    def requirements_db(self):
        return 'sum'

    def name(self):
        return 'mean'

class Count(Statistics):
    """ 
        Computes the number of values using the count
        obtained from the database.
    """

    def compute_db(self,columns,data,name):
        count = self.data2np(data[name],columns['count'])
        if len(count) == 0:
            return self.array(0)
        return self.array(np.sum(count))

    def requirements_db(self):
        return 'sum'

    def name(self):
        return 'count'

    def unit(self):
        return ''

    def moreIsBetter(self):
        return True

class SumSquared(Statistics):
    """ 
        Computes the sum of squares of values
        to store in the database as a temporary result
    """
    def compute_raw(self,variables,name,storer,record):
        variable = variables[name]
        self.store(storer,record,value=np.sum(variable*variable),count=variable.shape[0])

    def name(self):
        return 'sumsquare'

class RootMeanSquare(Statistics):
    """ 
        Computes the root mean square by summing the sums of 
        squares obtained from the database.
    """
    def compute_db(self,columns,data,name):
        value = self.data2np(data[name],columns['value'])
        count = self.data2np(data[name],columns['count'])
        if len(count) == 0:
            return self.array(self.missing_value)
        value = np.sum(value)
        count = np.sum(count)
        value = self.array(math.sqrt(value / count))
        return self.array(value)

    def requirements_db(self):
        return 'sumsquare'

    def name(self):
        return 'rms'
