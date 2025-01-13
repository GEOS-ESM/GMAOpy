import types
from pylab import *
from pylab import prctile
from gmaopy.netcdf.fieldreader import FieldReader

f = FieldReader('file.hdf')
directive = dict(
    level = [1000,500,300,100],
    latitude = {-40:50},
    longitude = {-20:200},
    date = 2010070812,
    parameter = 'u',
)
v = f.readFieldSet(directive,a = 2,b = 3)
print(v)
for h in v:
    print(h.multipleDimensions())
