import copy
from collections import defaultdict
import numpy.ma as ma
from semperpy.core.tools import nestedLoops,to_list,is_list,is_string,no_list
from semperpy.plot.plot import Plot
from gmaopy.obs.odsengine import ODSEngine
from gmaopy.obs.obsexpander import ObsExpander
from gmaopy.obs.oceanmasking import OceanMasking
from gmaopy.obs.odsstatistics import ODSStatistics

class ODSPlot(Plot):

    def distributeCurves(self,curves,what):
        combinations = []
        id = 0
        for curve in curves:
            curve = copy.copy(curve)
            curve.overwrite_from(self,exclude='filename')
            all = curve.data.distribute(self,what)
            for one in all:
                c = copy.copy(curve)
                c.data = one
                c['_id'] = one['_id']
                c.finalise()
                combinations.append(c)
                id += 1
        return combinations

    def variables(self,obs):
        return to_list(obs['variable'])

    def doRetrieve(self):
        curves = self.curves_
        masking = None
        for curve in curves:
            if is_list(curve.data['usage']):
                curve.data['usage'] = curve.data['usage'][0]
            curve.doRetrieve(self,self.me_)
        if not 'source' in self.data:
            raise RuntimeError('The keyword "source" is required when plotting data from ODS files')
        if self.data['source'] == 'odas':
            masking = OceanMasking()
        ODSEngine([ x.data for x in curves],self,self['staging_rate'],masking,self['ignore_missing_files'])
        groups = defaultdict(list)
        for curve in curves:
            groups[curve['_id']].append(curve) 
        ids = list(groups.keys())
        ids.sort()
        curves = []
        for id in ids:
            curve = copy.copy(groups[id][0])
            for variable in curve.data.variables(variable = 'all'):
                if len(groups[id]) > 1:
                    result = []
                    curve.data['kt'] = curve.data['o_kt']
                    curve.data['kx'] = curve.data['o_kx']
                    levtypes = set([ x.data['levtype'] for x in groups[id]])
                    if len(levtypes) == 1:
                        lengths = set([ len(x.data.variables(variable=variable)) for x in groups[id] ])
                        if len(lengths) != 1:
                            raise ValueError('Do not know how to handle same level type but different lengths')
                        result = groups[id][0].data.variables(variable=variable)
                        for g in groups[id][1:]:
                            r = g.data.variables(variable=variable)
                            for i in range(len(result)):
                                result[i] = ma.concatenate((result[i],r[i]))
                    else:
                        result = []
                        for x in groups[id]:
                            result += x.data.variables(variable=variable)
                    curve.data.variables(result,variable=variable)
            actor = ODSStatistics.create(to_list(curve.data['statistic'])[0])
            curve.data.value = actor(curve.data.variables(variable='all'))
            curves.append(curve)
        self.curves_ = curves
        self['curve'] = curves

    def processData(self,engine,date,ods,obs,filter,levelFilter,domain_filters,usage_filters):
        variables = self.variables(obs)
        values = defaultdict(list)
        if not 'level' in obs:
            obs['level'] = None
        usage = obs['usage']
        for level in tuple(to_list(obs['level'])):
            finalfilter = filter
            if levelFilter is not None and level is not None:
                finalfilter = (levelFilter == level) & filter
            for domain in to_list(obs['domain_name']):
                for variable in variables:
                    values[variable].append(engine.extractVariable(variable,ods,domain,domain_filters,usage,usage_filters,finalfilter))
        for variable in variables:
            if obs.hasVariable(variable):
                previous = obs.variables(variable = variable)
                obs.variables(previous + values[variable],variable = variable)
            else:
                obs.variables(values[variable],variable = variable)

