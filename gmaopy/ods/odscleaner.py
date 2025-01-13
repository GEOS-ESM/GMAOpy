from collections import defaultdict
import numpy as np
from semperpy.core.configure import Configure
from semperpy.core.configfile import ConfigFile
from semperpy.observations.observation import Observation

class ODSCleaner(object):
    
    def __init__(self,name):
        self.exclusions_ = None
        self.name_ = name

    def __call__(self,ods,kt_list):
        qcexcl = np.array(list(ods.extract('qcexcl').values()))
        exclusions = self.exclusions()
        if len(exclusions) > 0:
            kts = np.array(list(ods.extract('kt').values()))
            for var in exclusions.keys():
                variable = ods.extract(var).values()
                for kt in kt_list:
                    if kt in exclusions[var]:
                        max = exclusions[var][kt]
                        bad = np.argwhere(np.logical_and(np.logical_and(kts == kt,variable > max),qcexcl == 0))
                        if len(bad) > 0:
                            qcexcl[bad] = 3
        return Observation(qcexcl)

    def exclusions(self):
        if self.exclusions_ is None:
            configure = Configure('semperpy')
            filename = configure.file('%s_exclusions.def' % self.name_,'CONFIG','ods')
            if len(filename) > 0:
                self.exclusions_ = ConfigFile(filename[0])
                new = defaultdict(dict)
                for key,item in self.exclusions_.items():
                    for k,i in item.items():
                        new[key][int(k)] = int(i)
                self.exclusions_ = new
            else:
                self.exclusions_ = {}
        return self.exclusions_
