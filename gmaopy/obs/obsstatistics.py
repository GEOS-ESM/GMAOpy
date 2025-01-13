import math
import numpy as np
import numpy.ma as ma
from semperpy.core.decorators import abstractMethod
from gmaopy.stats.statistics import Statistics
from gmaopy.stats.commonstats import *

class CountObsAnl(Statistics):

    def compute_db(self,columns,data,name):
        ### Correction: multiple instrument combination impacts 20190516
        # Issue when calculating multiple kx-impact when one kx has an
        # obs dropout over the period in question. New calculation is
        # taking a weighted sum of individual kx impacts.
        if 'kx' in columns:
            kxs = set(d[columns['kx']] for d in data[name])

            if len(kxs) == 0:
                return self.array(self.missing_value)

            total_kx = {}
            for kx in kxs:
                total_kx[kx] = total_kx.get(kx, 0)
                # obtain dates for given kx
                dates = set(d[columns['date']] for d in data[name] if d[columns['kx']] == kx)

                if len(dates) == 0:
                    return self.array(self.missing_value)

                count = self.data2np([d for d in data[name] if d[columns['kx']] == kx], columns['count'])

                if len(count) == 0:
                    return self.array(self.missing_value)

                total_kx[kx] = self.array(np.sum(count) / len(dates))
            #print('new CountObsAnl', sum(total_kx.values()))
            return sum(total_kx.values())
        else:
            # old code
            dates = set()
            for d in data[name]:
                dates.add(d[columns['date']])
            if len(dates) == 0:
                return self.array(self.missing_value)
            count = self.data2np(data[name],columns['count'])
            if len(count) == 0:
                return self.array(self.missing_value)
            total = np.sum(count)
            #print('old CountObsAnl', self.array(total / len(dates)))
            return self.array(total / len(dates))

    def requirements_db(self):
        return 'sum'

    def name(self):
        return 'count_per_anl'

    def unit(self):
        return ''

    def moreIsBetter(self):
        return True

class CountObsAnlOld(Statistics):

    def compute_db(self,columns,data,name):
        dates = set()
        for d in data[name]:
            dates.add(d[columns['date']])
        if len(dates) == 0:
            return self.array(self.missing_value)
        count = self.data2np(data[name],columns['count'])
        if len(count) == 0:
            return self.array(self.missing_value)
        total = np.sum(count)
        #print('old CountObsAnl', self.array(total / len(dates)))
        return self.array(total / len(dates))

    def requirements_db(self):
        return 'sum'

    def name(self):
        return 'count_per_anl_old'

    def unit(self):
        return ''

    def moreIsBetter(self):
        return True

class Beneficial(Statistics):
    """ 
        Computes the number of values which are less than zero
        from ODS files. From the database it then divides the
        sum of the values by the total number of values.
    """

    def compute_raw(self,variables,name,storer,record):
        # mask_greater rejects anything which is greater than the value,
        # this keeps values below 0.0
        variable = variables[name]
        a = ma.masked_greater(variable,0.0)
        a = a.compressed()
        self.store(storer,record,value=a.shape[0],count=variable.shape[0])

    def compute_db(self,columns,data,name):
        value = self.data2np(data[name],columns['value'])
        count = self.data2np(data[name],columns['count'])
        if len(count) == 0:
            return self.array(self.missing_value)
        count = np.sum(count)
        result = self.array(np.sum(value) / count * 100)
        #print('beneficial', result)
        return result

    def name(self):
        return 'beneficial'

    def unit(self):
        return '%'

    def moreIsBetter(self):
        return True

class Rate(Statistics):
    """ 
        Computes the number of values using the count
        obtained from the database and divides it by 
        the total number of runs.
    """

    def compute_db(self,columns,data,name):
        ### Correction: multiple instrument combination impacts 20190516
        # Issue when calculating multiple kx-impact when one kx has an
        # obs dropout over the period in question. New calculation is
        # taking a weighted sum of individual kx impacts.
        if 'kx' in columns:
            kxs = set(d[columns['kx']] for d in data[name])

            if len(kxs) == 0:
                return self.array(self.missing_value)

            total_kx = {}
            for kx in kxs:
                total_kx[kx] = total_kx.get(kx, 0)
                # obtain dates for given kx
                dates = set(d[columns['date']] for d in data[name] if d[columns['kx']] == kx)

                if len(dates) == 0:
                    return self.array(self.missing_value)

                count = self.data2np([d for d in data[name] if d[columns['kx']] == kx], columns['value'])

                if len(count) == 0:
                    return self.array(self.missing_value)

                total_kx[kx] = self.array(np.sum(count) / len(dates))
            #print('new Rate', sum(total_kx.values()))
            return sum(total_kx.values())
        else:
            # old code
            dates = set()
            for d in data[name]:
                dates.add(d[columns['date']])
            if len(dates) == 0:
                return self.array(self.missing_value)
            count = self.data2np(data[name],columns['value'])
            if len(count) == 0:
                return self.array(self.missing_value)
            total = np.sum(count)
            #print('old Rate', self.array(total / len(dates)))
            return self.array(total / len(dates))

    def requirements_db(self):
        return 'sum'

    def name(self):
        return 'rate'

class RateOld(Statistics):
    """ 
        Computes the number of values using the count
        obtained from the database and divides it by 
        the total number of runs.
    """

    def compute_db(self,columns,data,name):
        dates = set()
        for d in data[name]:
            dates.add(d[columns['date']])
        if len(dates) == 0:
            return self.array(self.missing_value)
        count = self.data2np(data[name],columns['value'])
        if len(count) == 0:
            return self.array(self.missing_value)
        total = np.sum(count)
        #print('old Rate', self.array(total / len(dates)))
        return self.array(total / len(dates))

    def requirements_db(self):
        return 'sum'

    def name(self):
        return 'rate_old'

class FractionalImpact(Statistics):

    def compute_db(self,columns,data,name):
        # new fractional impact (uses patch from counts_per_anl/impact_per_anl)
        if 'kx' in columns:
            # calculate partial
            kxs = set(d[columns['kx']] for d in data[name])
            if len(kxs) == 0:
                return self.array(self.missing_value)
            partial_kx = {}
            for kx in kxs:
                partial_kx[kx] = partial_kx.get(kx, 0)
                # obtain dates for given kx
                dates = set(d[columns['date']] for d in data[name] if d[columns['kx']] == kx)

                if len(dates) == 0:
                    return self.array(self.missing_value)

                value = self.data2np([d for d in data[name] if d[columns['kx']] == kx], columns['value'])

                if len(value) == 0:
                    return self.array(self.missing_value)

                partial_kx[kx] = self.array(np.sum(value) / len(dates))
            partial = sum(partial_kx.values())

            # calculate total
            kxs = set(d[columns['kx']] for d in data['*'])
            if len(kxs) == 0:
                return self.array(self.missing_value)
            total_kx = {}
            for kx in kxs:
                total_kx[kx] = total_kx.get(kx, 0)
                # obtain dates for given kx
                dates = set(d[columns['date']] for d in data['*'] if d[columns['kx']] == kx)

                if len(dates) == 0:
                    return self.array(self.missing_value)

                value = self.data2np([d for d in data['*'] if d[columns['kx']] == kx], columns['value'])

                if len(value) == 0:
                    return self.array(self.missing_value)

                total_kx[kx] = self.array(np.sum(value) / len(dates))
            total = sum(total_kx.values())
            # total uses only region global - FIXED
            # look in obsdata.py for retrieval region modification
            if total == 0.:
                print('\nWARNING: Total sum impacts for global region not found in database.')
                print('Dates used for PARTIAL impact:')
                print(('\t' + str(sorted(set(d[2] for d in data[name])))))
                print('Dates used for TOTAL impact:')
                print(('\t' + str(sorted(set(d[2] for d in data['*'])))))
                print('')
                return self.array(self.missing_value)
            #print('new fractional impact', partial/total * 100.)
            return partial/total * 100.
        else:
            dates = set()
            for d in data[name]:
                dates.add(d[columns['date']])
            if len(dates) == 0:
                return self.array(self.missing_value)
            value = self.data2np(data[name],columns['value'])
            if len(value) == 0:
                return self.array(self.missing_value)
            partial = np.sum(value) / len(dates)
    
            # because the total of instruments (i.e., sum:*) have multiple
            # kxs, we have to separate them out to obtain a weighted sum
            #dates_list = []
            dates = set()
            for d in data['*']:
                dates.add(d[columns['date']])
                #dates_list.append(d[columns['date']]
            if len(dates) == 0:
                return self.array(self.missing_value)
            value = self.data2np(data['*'],columns['value'])
            # total uses only region global - FIXED
            # look in obsdata.py for retrieval region modification
            total = np.sum(value)
            if total == 0.:
                print('\nWARNING: Total sum impacts for global region not found in database.')
                print('Dates used for PARTIAL impact:')
                print(('\t' + str(sorted(set(d[2] for d in data[name])))))
                print('Dates used for TOTAL impact:')
                print(('\t' + str(sorted(set(d[2] for d in data['*'])))))
                print('')
                return self.array(self.missing_value)
            total = total / len(dates)
            #print('new fractional impact old code', self.array(partial/total) * 100.)
            return self.array(partial/total) * 100.

    def requirements_db(self):
        return ['sum','sum:*']

    def name(self):
        return 'fractional_impact'

    def unit(self):
        return '%'

class FractionalImpactOld(Statistics):

    def compute_db(self,columns,data,name):
        value = self.data2np(data[name],columns['value'])
        if len(value) == 0:
            return self.array(self.missing_value)
        partial = np.sum(value)
        value = self.data2np(data['*'],columns['value'])
        # total uses only region global - FIXED
        # look in obsdata.py for retrieval region modification
        total = np.sum(value)
        if total == 0.:
            print('\nWARNING: Total sum impacts for global region not found in database.')
            print('Dates used for PARTIAL impact:')
            print(('\t' + str(sorted(set(d[2] for d in data[name])))))
            print('Dates used for TOTAL impact:')
            print(('\t' + str(sorted(set(d[2] for d in data['*'])))))
            print('')
            return self.array(self.missing_value)
        #print('old fractional impact', self.array(partial/total) * 100.)
        return self.array(partial/total) * 100

    def requirements_db(self):
        return ['sum','sum:*']

    def name(self):
        return 'fractional_impact_old'

    def unit(self):
        return '%'

class NormalizedCost(Statistics):

    def compute_raw(self,variables,variable,storer,record,temp=None):
        variable_name = variable
        variable = variables[variable]
        if temp is not None:
            sigo = np.array(variables['xvec'][temp])
        else:
            sigo = np.array(variables['xvec'])
        nonzeros = np.nonzero(sigo)[0]
        # eliminate all entries where sigo is zero
#        print(nonzeros,"/n ******** /n",np.nonzero(sigo),"/n ******** /n", sigo )
        nonzero_sigo = sigo[nonzeros]
        variable = variable[nonzeros]
        value = variable / nonzero_sigo
        if temp is not None:
            try:
                value = value.compressed()
            except:
                pass
        self.store(storer,record,value=np.sum(value * value),count=variable.shape[0])

    def compute_db(self,columns,data,name):
        mean = self.create('obsstat','mean')
        #print('normalized cost', self.array(mean.compute_db(columns,data,name)))
        return self.array(mean.compute_db(columns,data,name))

    def requirements_raw(self):
        return ['var','xvec']

    def name(self):
        return 'normcost'

class EstimatedSigo(Statistics):

    def compute_raw(self,variables,variable,storer,record):
        oma = variables['oma']
        omf = variables['omf']
        if oma.shape == omf.shape and oma.shape != 0:
            self.store(storer,record,value=np.sum(oma * omf),count=oma.shape[0],variable='esigo')

    def compute_db(self,columns,data,name):
        value = self.data2np(data['esigo'],columns['value'])
        count = self.data2np(data['esigo'],columns['count'])
        if len(value) == 0:
            return self.array(Statistics.missing_value)
        #print('estimated sigo', self.array(math.sqrt(max(0,np.sum(value) / np.sum(count)))))
        return self.array(math.sqrt(max(0,np.sum(value) / np.sum(count))))

    def requirements_raw(self):
        return ['oma','omf']

    def requirements_db(self):
        return ['esigo:esigo']

    def name(self):
        return 'esigo'

class EstimatedSigb(Statistics):

    def compute_raw(self,variables,variable,storer,record):
        oma = variables['oma']
        omf = variables['omf']
        if oma.shape == omf.shape and oma.shape != 0:
            self.store(storer,record,value=np.sum(omf * omf) - np.sum(oma * omf),count=oma.shape[0],variable='esigb')

    def compute_db(self,columns,data,name):
        value = self.data2np(data['esigb'],columns['value'])
        if len(value) == 0:
            return self.array(Statistics.missing_value)
        count = self.data2np(data['esigb'],columns['count'])
        #print('estimated sigb', self.array(math.sqrt(max(0,np.sum(value) / np.sum(count)))))
        return self.array(math.sqrt(max(0,np.sum(value) / np.sum(count))))

    def requirements_raw(self):
        return ['oma','omf']

    def requirements_db(self):
        return ['esigb:esigb']

    def name(self):
        return 'esigb'

#-------------------------------------------------------------
# Here we register our statistic classes under the name
# they are known by the user.
#-------------------------------------------------------------
Statistics.register('obsstat','count',Count)
Statistics.register('obsstat','count_per_anl',CountObsAnl)
Statistics.register('obsstat','count_per_anl_old',CountObsAnlOld)
Statistics.register('obsstat','sum',Sum)
Statistics.register('obsstat','mean',Mean)
Statistics.register('obsstat','impact_per_ob',Mean)
Statistics.register('obsstat','sumsquare',SumSquared)
Statistics.register('obsstat','rms',RootMeanSquare)
Statistics.register('obsstat','beneficial',Beneficial)
Statistics.register('obsstat','rate',Rate)
Statistics.register('obsstat','rate_old',RateOld)
Statistics.register('obsstat','impact_per_anl',Rate)
Statistics.register('obsstat','impact_per_anl_old',RateOld)
Statistics.register('obsstat','fractional_impact_old',FractionalImpactOld)
Statistics.register('obsstat','fractional_impact',FractionalImpact)
Statistics.register('obsstat','normcost',NormalizedCost)
Statistics.register('obsstat','esigo',EstimatedSigo)
Statistics.register('obsstat','esigb',EstimatedSigb)
