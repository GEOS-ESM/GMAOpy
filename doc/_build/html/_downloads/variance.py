import math
import numpy as np
from gmaopy.stats.statistics import Statistics

class Variance(Statistics):

    def requirements_db(self):
        return ['sum','sumsquare']

    def name(self):
        return 'variance'

    def compute_db(self,columns, data, variable):
        values = self.split(data[variable],columns['statistic'])
        if len(values) != 2 or not 'sum' in values or not 'sumsquare' in values:
            raise ValueError('could not find the statistics needed to compute the variance')
        sum = np.sum(self.data2np(values['sum'],columns['value']))
        sum_count = np.sum(self.data2np(values['sum'],columns['count']))
        sumsquare = np.sum(self.data2np(values['sumsquare'],columns['value']))
        sumsquare_count = np.sum(self.data2np(values['sumsquare'],columns['count']))
        if sum_count != sumsquare_count:
            raise ValueError('Found a different number of sums and sum squares %d %d' % (sum_count,sumsquare_count))
        if sum_count == 1:   
            return self.array(self.missing_value)
        mean = sum / sum_count
        return self.array((sumsquare - (mean * mean)) / (sumcount - 1))

Statistics.register('obsstat','variance',Variance)
