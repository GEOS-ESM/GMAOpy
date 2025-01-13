import copy
import bisect
from collections import defaultdict
from semperpy.core.tools import to_list, nestedLoops
from semperpy.plot.document import document
from semperpy.core.configfile import ConfigFile
from semperpy.core.index import Index
from semperpy.slicing.arraygenerator import ArrayGenerator
from gmaopy.obs.obsplotdata import ObsPlotData
from gmaopy.obs.obsexpander import ObsExpander
from gmaopy.db.obrecord import OBRecord
from gmaopy.storage.reader import Reader
from gmaopy.stats.statistics import Statistics
from gmaopy.obs.obstexttemplate import ObsTextTemplate

class newObsData(ObsPlotData):
    def distribute(self, owner, what):
        isDoc = isinstance(owner, document)
        result = []
        if 'filename' in self:
            all = ObsExpander.expand_for_retrieval(self)
            if isDoc:
                self.assignLevels(all)

class ObsData(ObsPlotData):

    def distribute(self,owner,what):
        isDoc = isinstance(owner,document)
        result = []
        if 'filename' in self:
            all = ObsExpander.expand_for_retrieval(self)
            if isDoc:
                self.assignLevels(all)
            for one in all:
                result += one.distribute(owner,what)
        else:
            if isDoc:
                self.assignLevels(self)
            result =  super(ObsData,self).distribute(owner,what)
        if not isDoc:
            self.assignLevels(result)
        return result

    def category(self):
        return 'obsstat'

    def retrieve(self,owner,index_columns,columns,data_columns,statistic,actor):
        reader = Reader.create(self['storage'],self['database'])
        main_variable = self['variable']
        requirements = self.requirements(to_list(actor.requirements_db()),self['variable'])
        specs = None
        if 'datefile' in self:
            alldates, allexpvers = self.datesAndExpvers(self['datefile'], self['date'])
            self['date'] = []
        data = defaultdict(list)
        other = copy.copy(self)
        usage = set(to_list(other['usage']))
        if 'unused' in usage:
            other['usage'] = ['used','passive']
            other.negate('usage')
        for k,i in requirements.items():
            if k == '*':
                keys = ['kx','kt','levtype','level']
                for key in keys:
                    if key in other:
                        del(other[key])
                    other['domain_name'] = 'global'
            else:
                other['variable'] = k
            ### Correction: multiple instrument combination impacts 20190516
            # Issue when calculating multiple kx-impact when one kx has an
            # obs dropout over the period in question. New calculation is
            # taking a weighted sum of individual kx impacts.
            if len(self['kx']) > 1 and 'old' not in statistic and k != '*':
                if 'kx' not in columns:
                    columns.append('kx')
                    data_columns['kx'] = data_columns.get('kx', 5)
            for statindx in range(len(i)):
                other['statistic'] = Statistics.create(self.category(),i[statindx]).name()
                if 'datefile' in self:
                    for date,expver in zip(alldates,allexpvers):
                        other['date'] = date
                        self['date'] += date
                        other['expver'] = expver
                        ### Correction: multiple instrument combination impacts 20190516
                        # Issue when calculating multiple kx-impact when one kx has an
                        # obs dropout over the period in question. New calculation is
                        # taking a weighted sum of individual kx impacts.
                        #if 'per_anl' in actor.name() and 'old' not in actor.name():
                        if len(self['kx']) > 1 and 'old' not in statistic and k != '*': # and 'kx' in other:
                            other_kx = copy.copy(other)
                            for kx in other['kx']:
                                other_kx['kx'] = [kx]
                                data[k] += reader(other_kx,columns)
                        else:
                            data[k] += reader(other,columns)
                else:
                    ### Correction: multiple instrument combination impacts 20190516
                    # Issue when calculating multiple kx-impact when one kx has an
                    # obs dropout over the period in question. New calculation is
                    # taking a weighted sum of individual kx impacts.
                    #if 'per_anl' in actor.name() and 'old' not in actor.name():
                    if len(self['kx']) > 1 and 'old' not in statistic and k != '*': # and 'kx' in other:
                        other_kx = copy.copy(other)
                        for kx in other['kx']:
                            other_kx['kx'] = [kx]
                            data[k] += reader(other_kx,columns)
                    else:
                        data[k] += reader(other,columns)
        keys = index_columns
        retrieved = []
        if len(keys) == 0:
            retrieved = actor.compute_db(data_columns,data,main_variable)
        else:
            gen = ArrayGenerator() #missing_value=Statistics.missing_value) 
            indexes = {}
            for k in requirements:
                indexes[k] = Index(*keys)
                for d in data[k]:
                    params = {}
                    for key in keys:
                        params[key] = d[data_columns[key]]
                    indexes[k].insert(d,**params)
            combinations = {}
            shape = 1
            multi_shape = []
            for key in keys:
                ll = len(to_list(self[key]))
                shape *= ll
                multi_shape.append(ll)
                combinations[key] = self[key]
            result = gen.create((shape))
            all = nestedLoops(combinations,keys)
            i = 0
            for v in all:
                final = {}
                for k in requirements:
                    if k == '*':
                        for key in keys:
                            if key != 'date':
                                del(v[key])
                    final[k] = indexes[k].access(**v) 
                current = actor.compute_db(data_columns,final,main_variable)
                assert(len(current) == 1)
                result[i] = current[0]
                i += 1
            retrieved = gen.postProcess(result)
            if len(multi_shape) > 1:
                retrieved = ma.reshape(retrieved,multi_shape)
            if 'transform' in self:
                for t in self['transform']:
                    retrieved = t(self,retrieved)
        return retrieved

    def startRetrieve(self):
        actor = Statistics.create(self.category(),self['statistic'])
        actor.prepareProcessing(self)

    def stopRetrieve(self):
        actor = Statistics.create(self.category(),self['statistic'])
        actor.completeProcessing(self)

    def requirements(self,statistics,variable):
        result = defaultdict(list)
        for stat in statistics:
            l = stat.split(':')
            if len(l) == 2:
                statname = l[0]
                params = l[1].split(',')
                for param in params:
                    result[param].append(statname)
            elif len(l) == 1:
                result[variable].append(stat)
            else:
                raise IndexError('The statistic %s is badly formatted' % stat)
        return result

    def prefixName(self):
        return 'SEMPERPY','obstitles.def'

obsdata = ObsData
