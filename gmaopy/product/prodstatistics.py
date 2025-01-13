import math
import numpy as np
import numpy.ma as ma
from semperpy.core.decorators import abstractMethod
from gmaopy.stats.statistics import Statistics

class ProdStatistics(Statistics):

    @abstractMethod
    def compute_raw(self,variables,name,storer,record):
        pass

    @abstractMethod
    def compute_db(self,columns,data,variable):
        pass

    def name(self):
        pass

    def prepareData(self,variable):
        variable = ma.compressed(variable)
        variable = variable.flatten()
        return variable

class SumData(ProdStatistics):

    def compute_raw(self,variables,name,storer,record):
        variable = self.prepareData(variables[name])
        self.store(storer,record,value=np.sum(variable),count=variable.shape[0])

    def compute_db(self,columns,data,variable):
        v = self.data2np(data[variable],columns['value'])
        if len(v) == 0:
            return self.array(self.missing_value)
        return self.array(np.sum(v))

    def name(self):
        return 'sum'

class MeanData(SumData):
    """ 
        Computes the mean of values using the sum
        obtained from the database.
    """

    def compute_db(self,columns,data,variable):
        value = self.data2np(data,columns['value'])
        count = self.data2np(data,columns['count'])
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

#-------------------------------------------------------------
# Here we register our statistic classes under the name
# they are known by the user.
#-------------------------------------------------------------
ProdStatistics.register('product','sum',SumData)
ProdStatistics.register('product','mean',MeanData)
