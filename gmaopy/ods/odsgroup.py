import numpy as np
import numpy.ma as ma
from semperpy.observations.obsfilter import ObsFilter
from semperpy.observations.observation import Observation
from gmaopy.ods.ods import ODS

class ODSGroup(object):

    def __init__(self,files,masking):
        self.ods_ = []
        for file in files:
            self.ods_.append(ODS(file,masking=masking))

    def close(self):
        for ods in self.ods_:
            ods.close()

    def compile(self,expression,used_observations = True,**kargs):
        # if variables are passed in the kargs, they will be of the shape
        # of the concatenated values (probably returned by self.read(). 
        # Because we compile one file by one file,
        # we need to split those variables.
        variables = [ {} for x in self.ods_ ]
        for name,value in kargs.items():
            value = value.values()
            offset = 0
            for i,ods in enumerate(self.ods_):
                var = ods.read(name).values()
                chunk = value[offset:offset+var.shape[0]]
                offset += var.shape[0]
                variables[i][name] = Observation(chunk)
        filters = []
        for i,ods in enumerate(self.ods_):
            filters.append(ods.compile(expression,used_observations,**variables[i]).values())#list(ods.compile(expression,used_observations,**variables[i]).values()))
        return ObsFilter(self.concatenate(filters))

    def extract(self,name,filter = None):
        all = []
        for ods in self.ods_:
            all.append(ods.extract(name).values())#list(ods.extract(name).values()))
        variable = (self.concatenate(all))
        if filter is not None:
            variable = variable[filter.values()]#list(filter.values())]
        return Observation(variable)
    read = extract

    def concatenate(self,all):
        # np.concatenate does not preserve the masks, so ma.concatenate needs to be
        # called then the arrays are masked.
        module = np
        for value in all:
            if isinstance(value,ma.core.MaskedArray):
                module = ma
                break
        return module.concatenate(all)
