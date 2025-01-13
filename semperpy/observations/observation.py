import numpy as np
import semperpy.observations.observation

class Observation(object):

    def __init__(self,value = None, info = None):
        self.value_ = value
        self.info_ = info

    def values(self):
        return self.value_

    def info(self):
        return self.info_

    # delegate everything we don't know to numpy
    def __getattr__(self,attr):
        try:
            f = getattr(self.values(),attr)
        except AttributeError:
            raise AttributeError('Unknown attribute: %s' % attr)
        return f

    def __str__(self):
        return self.value_.__str__()

    def __call__(self,value = None):
        if value:
            if isinstance(value,semperpy.observations.observation.Observation):
                value = value.values()
            return self.values()[value]
        else:
            return self.value()

#--------- < generated automatically by make_src/observation_operators.py, do not edit ------------

    def __add__(self,other):
        if isinstance(other,Observation):
            return Observation(self.values() + other.values())
        else:
            return Observation(self.values() + other)
    __radd__ =  __add__ 

    def __iadd__(self,other):
        v = self.values()
        if isinstance(other,Observation):
            v += other.values()
        else:
            v += other
        return self 

    def __sub__(self,other):
        if isinstance(other,Observation):
            return Observation(self.values() - other.values())
        else:
            return Observation(self.values() - other)
    __rsub__ =  __sub__ 

    def __isub__(self,other):
        v = self.values()
        if isinstance(other,Observation):
            v -= other.values()
        else:
            v -= other
        return self 

    def __mul__(self,other):
        if isinstance(other,Observation):
            return Observation(self.values() * other.values())
        else:
            return Observation(self.values() * other)
    __rmul__ =  __mul__ 

    def __imul__(self,other):
        v = self.values()
        if isinstance(other,Observation):
            v *= other.values()
        else:
            v *= other
        return self 

    def __div__(self,other):
        if isinstance(other,Observation):
            return Observation(self.values() / other.values())
        else:
            return Observation(self.values() / other)
    __rdiv__ =  __div__ 

    def __idiv__(self,other):
        v = self.values()
        if isinstance(other,Observation):
            v /= other.values()
        else:
            v /= other
        return self 

    def __eq__(self,other):
        if isinstance(other,Observation):
            return Observation(self.values() == other.values())
        else:
            return Observation(self.values() == other) 

    def __ne__(self,other):
        if isinstance(other,Observation):
            return Observation(self.values() != other.values())
        else:
            return Observation(self.values() != other) 

    def __gt__(self,other):
        if isinstance(other,Observation):
            return Observation(self.values() > other.values())
        else:
            return Observation(self.values() > other) 

    def __lt__(self,other):
        if isinstance(other,Observation):
            return Observation(self.values() < other.values())
        else:
            return Observation(self.values() < other) 

    def __ge__(self,other):
        if isinstance(other,Observation):
            return Observation(self.values() >= other.values())
        else:
            return Observation(self.values() >= other) 

    def __le__(self,other):
        if isinstance(other,Observation):
            return Observation(self.values() <= other.values())
        else:
            return Observation(self.values() <= other)

    def __rsub__(self,other):
        v = - self.values()
        if isinstance(other,Observation):
            return Observation(v + other.values())
        else:
            return Observation(v + other) 

    def __rdiv__(self,other):
        v = 1 / self.values()
        if isinstance(other,Observation):
            return Observations(v * other.values())
        else:
            return Observation(v * other)
    __truediv__ = __div__ 

    def __and__(self,other):
        if isinstance(other,Observation):
            other = other.values()
        return Observation(np.logical_and(self.values(),other))


    def __or__(self,other):
        if isinstance(other,Observation):
            other = other.values()
        return Observation(np.logical_or(self.values(),other))


    def __invert__(self):
        return Observation(np.logical_not(self.values()))


    def __abs__(self):
        return Observation(self.values().__abs__())

#--------- generated automatically by make_src/observation_operators.py, do not edit > ------------

