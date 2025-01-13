from semperpy.core.tools import classof,mergedicts_keep,is_list
from semperpy.fields.containers.arraycontainer import ArrayContainer
from semperpy.fields.grid import Grid

class Field(object):

    def __init__(self,values,dimensions,metadata):
        self.values_ = values
        self.dimensions_ = dimensions
        self.metadata_ = metadata

    #----------------------------------------------------------------------------
    # Field data manipulation (it is anticipated that most of the time the
    # data will be a numpy array).
    #----------------------------------------------------------------------------
    def values(self):
        return self.values_()

    def data(self):
        return self.values_

    def shape(self):
        return self.values_.shape()

    def dimensions(self):
        return self.dimensions_

    def unload(self):
        self.values_.unload()
        return self

    def multipleDimensions(self):
        result = []
        names = list(self.dimensions_)
        names.reverse()
        for name in names:
            i = self.metadata_[name]
            if is_list(i) and len(i) > 1:
                result.append(name)
        return result

    def grid(self):
        return Grid(self.metadata_['latitude'],self.metadata_['longitude'])

    def metadata(self):
        return self.metadata_

    def get(self,name):
        return self.metadata_[name]

    def set(self,name,value):
        self.metadata_[name] = value
        return self

    def __contains__(self,key):
        return key in self.metadata_

    def __getattr__(self,attr):
        return getattr(list(self.values()),attr)

    def __len__(self):
        return len(list(self.values()))

    def extract_subdomain(self,domain):
        return self.grid_.extract_subdomain(domain,list(self.values()),self.get('missing_value'))

    def extract_subdomain_array(self,array,domain):
        return self.grid_.extract_subdomain(domain,array,self.get('missing_value'))

    def subField(self,domain):
        values = self.grid_.extract_subdomain(domain,list(self.values()),self.get('missing_value'))
        grid = self.grid_.extract_grid(domain)
        return NField(ArrayContainer(values),grid,self.metadata())

    def sqrt(self):
        return classof(self)(ArrayContainer(self.values_.sqrt()),self.dimensions(),self.metadata())
        

#--------- < generated automatically by make_src/field_operators.py, do not edit ------------

    def __add__(self,other):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(list(self.values()) + list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(list(self.values()) + other),self.dimensions(),self.metadata())
    __radd__ =  __add__ 

    def __iadd__(self,other):
        v = list(self.values())
        if isinstance(other,Field):
            v += list(other.values())
        else:
            v += other
        return self 

    def __sub__(self,other):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(list(self.values()) - list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(list(self.values()) - other),self.dimensions(),self.metadata())
    __rsub__ =  __sub__ 

    def __isub__(self,other):
        v = list(self.values())
        if isinstance(other,Field):
            v -= list(other.values())
        else:
            v -= other
        return self 

    def __mul__(self,other):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(list(self.values()) * list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(list(self.values()) * other),self.dimensions(),self.metadata())
    __rmul__ =  __mul__ 

    def __imul__(self,other):
        v = list(self.values())
        if isinstance(other,Field):
            v *= list(other.values())
        else:
            v *= other
        return self 

    def __div__(self,other):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(list(self.values()) / list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(list(self.values()) / other),self.dimensions(),self.metadata())
    __rdiv__ =  __div__ 

    def __idiv__(self,other):
        v = list(self.values())
        if isinstance(other,Field):
            v /= list(other.values())
        else:
            v /= other
        return self 

    def __floordiv__(self,other):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(list(self.values()) // list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(list(self.values()) // other),self.dimensions(),self.metadata())
    __rfloordiv__ =  __floordiv__ 

    def __ifloordiv__(self,other):
        v = list(self.values())
        if isinstance(other,Field):
            v //= list(other.values())
        else:
            v //= other
        return self 

    def __mod__(self,other):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(list(self.values()) % list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(list(self.values()) % other),self.dimensions(),self.metadata())
    __rmod__ =  __mod__ 

    def __imod__(self,other):
        v = list(self.values())
        if isinstance(other,Field):
            v %= list(other.values())
        else:
            v %= other
        return self 

    def __eq__(self,other):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(list(self.values()) == list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(list(self.values()) == other),self.dimensions(),self.metadata())
    __req__ =  __eq__ 

    def __ieq__(self,other):
        v = list(self.values())
        if isinstance(other,Field):
            v == list(other.values())
        else:
            v == other
        return self 

    def __ne__(self,other):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(list(self.values()) != list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(list(self.values()) != other),self.dimensions(),self.metadata())
    __rne__ =  __ne__ 

    def __ine__(self,other):
        v = list(self.values())
        if isinstance(other,Field):
            v != list(other.values())
        else:
            v != other
        return self 

    def __gt__(self,other):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(list(self.values()) > list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(list(self.values()) > other),self.dimensions(),self.metadata())
    __rgt__ =  __gt__ 

    def __igt__(self,other):
        v = list(self.values())
        if isinstance(other,Field):
            v >= list(other.values())
        else:
            v >= other
        return self 

    def __lt__(self,other):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(list(self.values()) < list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(list(self.values()) < other),self.dimensions(),self.metadata())
    __rlt__ =  __lt__ 

    def __ilt__(self,other):
        v = list(self.values())
        if isinstance(other,Field):
            v <= list(other.values())
        else:
            v <= other
        return self 

    def __ge__(self,other):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(list(self.values()) >= list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(list(self.values()) >= other),self.dimensions(),self.metadata())
    __rge__ =  __ge__ 

    def __ige__(self,other):
        v = list(self.values())
        if isinstance(other,Field):
            v >= list(other.values())
        else:
            v >= other
        return self 

    def __le__(self,other):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(list(self.values()) <= list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(list(self.values()) <= other),self.dimensions(),self.metadata())
    __rle__ =  __le__ 

    def __ile__(self,other):
        v = list(self.values())
        if isinstance(other,Field):
            v <= list(other.values())
        else:
            v <= other
        return self 

    def __rsub__(self,other):
        v = - list(self.values())
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(v + list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(v + other),self.dimensions(),self.metadata()) 

    def __rdiv__(self,other):
        v = 1 / list(self.values())
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(v * list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(v * other,self.dimensions()),self.metadata())
    __truediv__ = __div__ 

    def __rdiv__(self,other):
        v = 1 // list(self.values())
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(v * list(other.values())),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(v * other),self.dimensions(),self.metadata()) 

    def __pow__(self,x):
        if isinstance(other,Field):
            return classof(self)(ArrayContainer(pow(list(self.values()),list(other.values()))),self.dimensions(),self.metadata())
        else:
            return classof(self)(ArrayContainer(pow(list(self.values()),other)),self.dimensions(),self.metadata()) 

    def __ipow__(self,x):
        v = list(self.values())
        if isinstance(other,Field):
            v.__ipow__(list(other.values()))
        else:
            v.__ipow__(other)
        return self 

    def __neg__(self):
        v = list(self.values())
        return classof(self)(-list(self.values()),self.dimensions(),self.metadata()) 

    def __abs__(self):
        v = list(self.values())
        return classof(self)(ArrayContainer(list(self.values()).__abs__()),self.dimensions(),self.metadata()) 

    def __pos__(self):
        v = list(self.values())
        return classof(self)(ArrayContainer(list(self.values()).__pos__()),self.dimensions(),self.metadata()) 

    def __invert__(self):
        v = list(self.values())
        return classof(self)(ArrayContainer(list(self.values()).__invert__()),self.dimensions(),self.metadata()) 

#--------- generated automatically by make_src/field_operators.py, do not edit > ------------
