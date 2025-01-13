import numpy as np

class Array(np.ndarray):
    
    def __bool__(self):
        return True

    def __and__(self,other):
        return np.logical_and(self,other)

    def __or__(self,other):
        return np.logical_and(self,other)

class SelectionVariable(object):

    def __init__(self,file,name):
        self.file_ = file
        self.name_ = name
        self.var_ = None

    def variable(self):
        if self.var_ == None:
            self.var_ = self.readVariable(self.file_,self.name_)
        return self.var_

    def readVariable(self,file,name):
        p = file.variables[name][:]
        v = Array(p.shape,p.dtype,p)
        try:
            a = getattr(file.variables[name],'add_offset')
                        v = v.astype(np.float32) + a
        except:
            pass
        try:
                        a = getattr(file.variables[name],'scale_factor')
                        v = v.astype(np.float32) * a
        except:
            pass
        return v

    def __lt__(self,other):
        if isinstance(other,SelectionVariable):
            return self.variable() < other.variable()
        else:
            return self.variable() < other

    def __gt__(self,other):
        if isinstance(other,SelectionVariable):
            return self.variable() > other.variable()
        else:
            return self.variable() > other

    def __le__(self,other):
        if isinstance(other,SelectionVariable):
            return self.variable() <= other.variable()
        else:
            return self.variable() <= other

    def __ge__(self,other):
        if isinstance(other,SelectionVariable):
            return self.variable() >= other.variable()
        else:
            return self.variable() >= other

    def __eq__(self,other):
        if isinstance(other,SelectionVariable):
            return self.variable() == other.variable()
        else:
            return self.variable() == other

    def __ne__(self,other):
        if isinstance(other,SelectionVariable):
            return self.variable() != other.variable()
        else:
            return self.variable() != other
