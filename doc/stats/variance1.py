from gmaopy.stats.statistics import Statistics

class Variance(Statistics):

    def name(self):
        return 'variance'

    def requirements_db(self):
        return ['sum','sumsquare']

Statistics.register('obsstat','variance',Variance)
