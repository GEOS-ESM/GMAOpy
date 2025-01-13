import re

template1 = """
    def __%op_name%__(self,other):
        if isinstance(other,Observation):
            return Observation(self.values() %op% other.values())
        else:
            return Observation(self.values() %op% other)
    __r%op_name%__ =  __%op_name%__ """

template2 = """
    def __i%op_name%__(self,other):
        v = self.values()
        if isinstance(other,Observation):
            v %op%= other.values()
        else:
            v %op%= other
        return self """

template3 = """
    def __%op_name%__(self,other):
        if isinstance(other,Observation):
            return Observation(self.values() %op% other.values())
        else:
            return Observation(self.values() %op% other) """

_rsub = """
    def __rsub__(self,other):
        v = - self.values()
        if isinstance(other,Observation):
            return Observation(v + other.values())
        else:
            return Observation(v + other) """

_rdiv = """
    def __rdiv__(self,other):
        v = 1 / self.values()
        if isinstance(other,Observation):
            return Observations(v * other.values())
        else:
            return Observation(v * other)
    __truediv__ = __div__ """

_and = """
    def __and__(self,other):
        if isinstance(other,Observation):
            other = other.values()
        return Observation(np.logical_and(self.values(),other))
"""

_or = """
    def __or__(self,other):
        if isinstance(other,Observation):
            other = other.values()
        return Observation(np.logical_or(self.values(),other))
"""

_invert = """
    def __invert__(self):
        return Observation(np.logical_not(self.values()))
"""

_abs = """
    def __abs__(self):
        return Observation(self.values().__abs__())
"""

bin_ops = dict(
    add = '+',
    sub = '-',
    mul = '*',
    div = '/',
    eq  = '==',
    ne  = '!=',
    gt  = '>',
    lt  = '<',
    ge  = '>=',
    le  = '<='
)
bin_order = ['add','sub','mul','div']
logical_order = ['eq','ne','gt','lt','ge','le']
if len(bin_order + logical_order) != len(bin_ops):
    raise ValueError('Some keys missing in the bin_order list')

print("#--------- < generated automatically by make_src/observation_operators.py, do not edit ------------")
for key in bin_order:
    op_name = key
    op = bin_ops[key]
    s = re.sub('%op_name%',op_name,template1)
    s = re.sub('%op%',op,s)
    print(s)
    s = re.sub('%op_name%',op_name,template2)
    s = re.sub('%op%',op,s)
    s = re.sub('==','=',s)
    print(s)
for key in logical_order:
    op_name = key
    op = bin_ops[key]
    s = re.sub('%op_name%',op_name,template3)
    s = re.sub('%op%',op,s)
    print(s)
print(_rsub)
print(_rdiv)
print(_and)
print(_or)
print(_invert)
print(_abs)
print("#--------- generated automatically by make_src/observation_operators.py, do not edit > ------------")
