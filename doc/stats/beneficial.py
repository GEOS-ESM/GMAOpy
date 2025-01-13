from gmaopy.stats.statistics import Statistics

class Beneficial(Statistics):
    """ 
        Computes the number of values which are less than zero
        from ODS files. From the database it then divides the
        sum of the values by the total number of values.
    """

    def name(self):
        return 'beneficial'

    def unit(self):
        return '%'

    def moreIsBetter(self):
        return True

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
        return result

Statistics.register('obsstat','beneficial',Beneficial)
