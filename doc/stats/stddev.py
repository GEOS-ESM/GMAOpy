import math
from variance import Variance

class StandardDeviation(Variance):

    def name(self):
        return 'stddev'

    def compute_db(self,columns, data, variable):
        result = super(StandardDeviation,self).compute_db(columns,data,variable)
        # we don't want to return the square root of missing value, it would mess things up
        if result[0] != self.missing_value:
            result =  self.array(math.sqrt(result))
        return result


Variance.register('obsstat','stddev',StandardDeviation)
