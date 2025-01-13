import numpy as np
from semperpy.core.tools import ErrorCreator
from semperpy.slicing.cf10.leveldimension import LevelDimension

variable = np.array([1000,975,950,925,900,875,850,825,800,750,700,650,600,550,500,450, 400, 350, 300, 250, 200, 150, 100, 70, 50, 40, 30, 20, 10, 7,5,3, 2, 1, 0.400000005960464, 0.200000002980232])
name = 'dim'
dim = LevelDimension(name,'official',variable)

print()
error = ErrorCreator(Exception)
print('testing dimension SortedDescendingDimension.....')
print()
n = dim.name()
print('name:', n)
if n != name:
    error('method name returned the wrong value')
w = variable[1:4]
v = dim.slice(slice(1,4,1))
print('slice:',v)
x = v == w
if not x.all():
    error('slice returned a wrong array')
x = dim.cache_[dim.hash_slice(slice(1,4,1))] == v
print('cache:',x)
if not x:
    error('caching did not work')
lim = dim.limits()
print('limits:',lim)
if list(lim) != [1000,0.200000002980232]:
    error('limits were returned wrong')
s = dim.findSlice([500,100])
print(s)
c = [slice(14, 15, 1), slice(22, 23, 1)]
if s != c:
    error('slice 1 failed')
s = dim.findSlice({970:250})
print(s)
c = [slice(1, 20, 1)]
if s != c:
    error('slice 2 failed')
s = dim.findSlice({675:8})
print(s)
c = [slice(10, 30, 1)]
if s != c:
    error('slice 3 failed')
try:
    s = dim.findSlice([1000,500,250,2000])
except IndexError:
    ok = True
if not ok:
    error('findSlice should have raise an exception for an unknown value')
error.check()
print()
print('all tests succeded for descending sorted dimension')
