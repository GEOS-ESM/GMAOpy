import re

template1 = """
    def __%op_name%__(self,other):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(self.values() %op% other.values()),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(self.values() %op% other),self.dimensions(),self.metadata())
    __r%op_name%__ =  __%op_name%__ """

template2 = """
    def __i%op_name%__(self,other):
        v = self.values()
        if isinstance(other,Field):
            v %op%= other.values()
        else:
            v %op%= other
        return self """

rsub = """
    def __rsub__(self,other):
        v = - self.values()
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(v + other.values()),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(v + other),self.dimensions(),self.metadata()) """

rdiv = """
    def __rdiv__(self,other):
        v = 1 / self.values()
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(v * other.values()),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(v * other,self.dimensions()),self.metadata())
    __truediv__ = __div__ """

rfloordiv = """
    def __rdiv__(self,other):
        v = 1 // self.values()
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(v * other.values()),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(v * other),self.dimensions(),self.metadata()) """
        
bin_ops = dict(
    add = '+',
    sub = '-',
    mul = '*',
    div = '/',
    floordiv = '//',
    mod = '%',
    eq  = '==',
    ne  = '!=',
    gt  = '>',
    lt  = '<',
    ge  = '>=',
    le  = '<='
)
bin_order = ['add','sub','mul','div','floordiv','mod','eq','ne','gt','lt','ge','le']
if len(bin_order) != len(bin_ops):
    raise ValueError('Some keys missing in the bin_order list')

pow = """
    def __pow__(self,x):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(pow(self.values(),other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(pow(self.values(),other)),self.dimensions(),self.metadata()) """

ipow = """
    def __ipow__(self,x):
        v = self.values()
        if isinstance(other,Field):
            v.__ipow__(other.values())
        else:
            v.__ipow__(other)
        return self """

neg = """
    def __neg__(self):
        v = self.values()
        return classof(self)(-self.values(),self.dimensions(),self.metadata()) """

abs = """
    def __abs__(self):
        v = self.values()
        return classof(self)(ArrayContainer(self.values().__abs__()),self.dimensions(),self.metadata()) """

invert = """
    def __invert__(self):
        v = self.values()
        return classof(self)(ArrayContainer(self.values().__invert__()),self.dimensions(),self.metadata()) """

pos = """
    def __pos__(self):
        v = self.values()
        return classof(self)(ArrayContainer(self.values().__pos__()),self.dimensions(),self.metadata()) """


print("#--------- < generated automatically by make_src/field_operators.py, do not edit ------------")
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
print(rsub)
print(rdiv)
print(rfloordiv)
print(pow)
print(ipow)
print(neg)
print(abs)
print(pos)
print(invert)
print("#--------- generated automatically by make_src/field_operators.py, do not edit > ------------")
