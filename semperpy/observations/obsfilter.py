from semperpy.observations.observation import Observation

class ObsFilter(Observation):

    def __call__(self,value = None):
        if value:
            if isinstance(value,Observation):
                value = value.values()
            return value[self.values()]
        else:
            return self.values()

    def notImplemented(self):
        raise NotImplementedError('This method cannot be applied to this object, it contains only boolean values')

    __add__ = notImplemented
    __radd__ = notImplemented
    __iadd__ = notImplemented
    __sub__ = notImplemented
    __rsub__ = notImplemented
    __isub__ = notImplemented
    __mul__ = notImplemented
    __rmul__ = notImplemented
    __imul__ = notImplemented
    __div__ = notImplemented
    __rdiv__ = notImplemented
    __idiv__ = notImplemented
