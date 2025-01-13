import numpy as np
import numpy.ma as ma
from semperpy.observations.observation import Observation

class ODSVariable(Observation):
    
    def __init__(self,name,file,actualSize = None, masking = None):
        super(ODSVariable,self).__init__()
        self.file_ = file
        self.value_ = name
        self.var_ = None
        self.loaded_ = False
        self.actualSize_ = actualSize
        self.masking_ = masking

    def values(self):
        if not self.loaded_:
            self.var_ = self.readVariable(self.file_,self.value_)
            self.loaded_ = True
        return self.var_

    def readVariable(self,file,name):
        v = file.variables[name][:]
        if self.masking_ is None:
            try:
                a = getattr(file.variables[name],'missing_value')
                v = ma.masked_values(v,a,copy=False,shrink=True)
            except:
                v = np.array(v)
              # v = ma.masked_values(v,-32767,copy=False,shrink=True)
        else:
            v = self.masking_(v,name,file)
        try:
            a = getattr(file.variables[name],'scale_factor')
            v = v.astype(np.float32) * a
        except:
            pass
        try:
            a = getattr(file.variables[name],'add_offset')
            v = v.astype(np.float32) + a
        except:
            pass
        v = v.flatten()
        if self.actualSize_ is not None:
            v = v[0:self.actualSize_]
        return v
