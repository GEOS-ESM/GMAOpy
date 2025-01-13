import copy
import numpy as np
from semperpy.core.tools import to_list
from semperpy.core.index import Index
from semperpy.directive.directive import Directive
from gmaopy.obs.odsengine import ODSEngine
from gmaopy.db.obrecord import OBRecord
from gmaopy.stats.statistics import Statistics
from gmaopy.obs.obsexpander import ObsExpander
from gmaopy.obs.oceanmasking import OceanMasking
from gmaopy.obs.obsdata import ObsData
from gmaopy.storage.storer import StorerCollection

class ObsStat(Directive):

    category_ = 'obsstat'

    def __init__(self,*args,**kargs):
        super(ObsStat,self).__init__(*args,**kargs)
        self.checkLanguage()
        self.storers_ = StorerCollection(self['storage'],write = True,**self)
        self.record_ = OBRecord()
        observations = self.observationList()
        masking = None
        if self['source'] == 'odas':
            masking = OceanMasking()
        ODSEngine(observations,self,self['staging_rate'],masking,self['ignore_missing_files']) # code fails here
        self.storers_.flush()

    def observationList(self):
        observations = []
        unique = set()
        if not 'observation' in self or len(self['observation']) == 0:
            obs = ObsData()
            self['observation'] = ObsExpander.all_observations(obs)
        for obs in self['observation']:
            obs.inherit_from(self,exclude = ['observation'])
            observations += ObsExpander.expand_for_storage(obs,unique)
        return observations

    def processData(self,engine,date,ods,obs,filter,levelFilter,domain_filters,usage_filters):
        statistics,separate,variables = self.requirements(obs['statistic'],obs['variable'])
        record = copy.copy(self.record_)
        record.overwrite_from(obs)
        record['date'] = date
        if 'output_expver' in obs and obs['output_expver'] is not None:
            record['expver'] = obs['output_expver']
        usage = obs['usage']
        if usage == 'unused':
            usage = usage_filters['unused_list']
        else:
            usage = to_list(usage)
        indexes = {}
        temp = {}
        for variable in variables:
            index = {}
            indexes[variable] = Index('level','domain_name','usage')
            for level in obs['level']:
                finalfilter = filter
                if levelFilter is not None:
                    finalfilter = (levelFilter == level) & filter
                for domain in obs['domain_name']:
                    for use in usage:
                        var = engine.extractVariable(variable,ods,domain,domain_filters,use,usage_filters,finalfilter)
                        try:
                            f = getattr(var, 'compressed')
                            newvar = var.compressed()
                            if len(var) != len(newvar):
                                temp[variable+str(level)+domain+use] = temp.get(variable+str(level)+domain+use, False == var.mask)
                            var = newvar
                        except AttributeError:
                            pass
                        indexes[variable].insert(var,level=level,domain_name=domain,usage=use)
        blah = None
        for level in obs['level']:
            record['level'] = level
            for domain in obs['domain_name']:
                for key_,val_ in domain_filters[domain].items():
                    if key_ != 'filter':
                        record[key_] = val_
                for use in usage:
                    record = copy.copy(record)
                    record['usage'] = use
                    vars = {}
                    for v in variables:

                        vars[v] = indexes[v].constrained_access(level=level,domain_name=domain,usage=use)
                        if v+str(level)+domain+use in temp:
                            blah = temp[v+str(level)+domain+use]
                    self.handleStatistics(record,vars,obs,statistics,separate,blah) 
                    blah = None
        del(temp)
        del(blah)

    def handleStatistics(self,record,vars,obs,statistics,separate,temp=None):
        for variable in obs['variable']:
            record['variable'] = variable
            for statistic in statistics:
                vars[variable] = np.array(vars[variable])
                if vars[variable].shape[0] == 0:
                    record['statistic'] = statistic
                    record['value'] = Statistics.missing_value
                    record['count'] = 0
                else:
                    actor = Statistics.create(self.category_,statistic)
                    record['statistic'] = actor.name()
                    if temp is not None and actor.name() in 'normcost':
                        actor.compute_raw(vars,variable,self.storers_,record,temp)
                    else:
#                        print('BEFORE COMPUTE RAW', variable, vars[variable])
                        actor.compute_raw(vars,variable,self.storers_,record)
        for statistic in separate:
            actor = Statistics.create(self.category_,statistic)
            record['statistic'] = actor.name()
#            print('BEFORE COMPUTE RAW SEPERATE', statistic)
            actor.compute_raw(vars,None,self.storers_,record) # self,variables,name,storer,record

    def variables(self,obs):
        dummy1,dummy2,variables = self.requirements(obs['statistic'],obs['variable'])
        return variables
        
    def requirements(self,stats,variables):
        statistics = set()
        for s in stats:
            actor = Statistics().create(self.category_,s)
            dependencies = to_list(actor.requirements_db())
            for v in dependencies:
                l = v.split(':')
                statistics.add(l[0])
        variables = set(variables)
        inloop = set()
        for s in statistics:
            actor = Statistics.create(self.category_,s)
            reqs = to_list(actor.requirements_raw())
            for var in reqs:
                if var == 'var':
                    inloop.add(s)
                else:
                    variables.add(var)
        specials = statistics.difference(inloop)
        return list(inloop),list(specials),list(variables)

obsstat = ObsStat
