import math
import re
from collections import defaultdict
import numpy as np
import numpy.ma as ma
from netCDF4 import Dataset
from semperpy.core.tools import to_list, apply_type, mergedicts_overwrite
from semperpy.core.date import Date
from semperpy.observations.obsfilter import ObsFilter
from semperpy.observations.observation import Observation
from gmaopy.ods.levelfilter import LevelFilter
from gmaopy.ods.odsvariable import ODSVariable

class ODS(object):
    
    stdlevels_ = (5.0,7.0,10.0,20.0,30.0,50.0,70.0,100.0,150.0,200.0,250.0,300.0,400.0,500.0,700.0,850.0,925.0,1000.0)
    pl_level_cache_ = defaultdict(dict)

    #-------------------------------------------------------------------
    # Reads ods files
    #-------------------------------------------------------------------
    def __init__(self,filename,masking = None):
        self.masking_ = masking
        try:
            self.file_ = Dataset(filename)
        except IOError as e:
            raise
            raise IOError(e.message + filename)
        self.variables_ = {}
        self.levels_ = None
        self.filename_ = filename
        self.synops_ = self.findSynopticTimes(self.file_)
        if len(self.synops_) > 1:
            raise SystemError('ODS only handles files with one synoptic time for the moment')
        self.actualSize_ = self.arrayActualSize(self.file_)
        self.cache_ = {}
        # we do the offset, masking and scaling ourselves so that
        # we are in control of array types and array manipulation
        for v in self.file_.variables.values():
            v.set_auto_maskandscale(False) 

    def close(self):
        self.file_.close()

    def arrayActualSize(self,file):
        batchlen = len(file.dimensions['batchlen'])
        date = list(self.synops_.keys())[0]
        return self.synops_[date]['length']

    def findSynopticTimes(self,file):
        nsyn = len(file.dimensions['nsyn'])
        syn_inc = 24 / nsyn
        syn_beg = file.variables['syn_beg']
        first_day = Date(re.sub('-','',syn_beg.reference_date)) + int(syn_beg.first_julian_day - syn_beg.value_at_reference_date)
        ndays = syn_beg.latest_julian_day - syn_beg.first_julian_day + 1
        begin = file.variables['syn_beg']
        length = file.variables['syn_len']
        synops = {}
        date = first_day
        for day in range(ndays):
            for syn in range(nsyn):
                if length[day,syn] > 0:
                    synops[date.intvalue() * 100 + syn * syn_inc] = dict(
                        begin = begin[day,syn] - 1,
                        length = length[day,syn]
                    )
            date += 1
        return synops

    def compile(self,expression,used_observations = True,**kargs):
        # we force the filter to only read observations which were used unless the user
        # forces the used_observations to False.
        if used_observations:
            if re.match('qcexcl',expression):
                raise ValueError('ODS.compile method, conflict: the parameter used_observations is set to True, but the variable "qcexcl" is included in the expression')
            else:
                expression = '(%s) & (qcexcl == 0)' % expression
        result = eval(expression,None,mergedicts_overwrite(self.variableDict(),kargs))
        return ObsFilter(result.values()) #,self.filename_)

    def variableDict(self):
        if len(self.variables_) == 0:
            for name in self.file_.variables:
                self.variables_[name] = ODSVariable(name,self.file_,self.actualSize_,masking=self.masking_)
        return self.variables_

    def extract(self,name,filter = None):
        if not name in self.file_.variables:
            raise ValueError('Sorry, variable %s does not exist in this file' % name)
        if name in self.cache_:
            v = self.cache_[name]
        else:
            v = ODSVariable(name,self.file_,self.actualSize_,masking=self.masking_)
            self.cache_[name] = v
        v = v.values()
        if filter is not None:
            if isinstance(filter,ObsFilter) or isinstance(filter,Observation):
                filter = filter.values()
            # when the filter is a masked array with all values missing, it seems that
            # v = v[filter] return some values while it should return an empty array.
            if isinstance(filter,ma.MaskedArray):
                if filter.mask.all():
                    return Observation(np.ndarray((0)))
            if v.shape != filter.shape:
                raise ValueError('arrays of different shapes, cannot filter')
            v = v[filter]
        return Observation(v)
    read = extract

    def sampleLevels(self,variable_name = 'lev',levels = None,bins = None):
        if levels is None:
            levels = np.array(list(self.extract(variable_name).values()))
        if bins is None or len(bins) < len(self.stdlevels_):
            bins = self.stdlevels_
        bins = list(bins)
        bins.sort()
        if not tuple(bins) in self.pl_level_cache_[self.filename_]:
            logs = []
            for level in bins:
                logs.append(np.abs(np.log(levels / level)))
            logs = np.column_stack(logs)
            for i in range(logs.shape[0]):
                minimum = np.argmin(logs[i])
                levels[i] = bins[minimum]
            result =  LevelFilter(levels,bins,self.filename_)
            self.pl_level_cache_[self.filename_][tuple(bins)] = result
        return self.pl_level_cache_[self.filename_][tuple(bins)]

    def sampleLinearLevels(self,variable_name = 'lev',levels = None,bins = None):
        if levels is None:
            levels = np.array(list(self.extract(variable_name).values()))
        diffs = []
        for level in bins:
            diffs.append(np.abs(levels - level))
        diffs = np.column_stack(diffs)
        for i in range(diffs.shape[0]):
            minimum = np.argmin(diffs[i])
            levels[i] = bins[minimum]
        return LevelFilter(levels,bins,self.filename_)

    def validateObsFilter(self,filter):
        if self.filename_ != filter.info():
            raise ValueError('The filter provided was computed on a different file')
                
    def validateLevelFilter(self,levels,levelfilter):
        if self.filename_ != levelfilter.filename():
            raise ValueError('The level filter provided was computed on a different file')
        levelist = set(levelfilter.levelist())
        levels = to_list(levels)
        for level in levels:
            if not level in levelist:
                raise ValueError('The requested levels (%s) do not match the levels used to build the level filter (%s)' % (', '.join(levels),', '.join(list(levelist))))
