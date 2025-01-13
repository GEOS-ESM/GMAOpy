try:
    from grads import GrADS
except:
    raise ImportError('pygrads doesn\'t seem to be installed.\nCannot run the test.')
import os
import gmaopy.netcdf
from semperpy.netcdf.file import File

datapath = os.getenv('SEMPERPY_TESTDATA')
if not datapath:
    raise SystemError('The variable SEMPERPY_TESTDATA is not defined. It should point to the SemperPy test dataset')
reader = File(datapath + '/an.hdf')
ga = GrADS(Echo=False,Window=False)
fh = ga.open(datapath + '/an.hdf')
ga('set time 0Z10jul2010 0Z10jul2010')
ga('set lon -180.0 179.333333')
ga('set lat -90 90')
ga('set lev 500')
v = ga.expr('u')
print()
print("pygrads")
print(v.shape)
print(v.mean())

directive = dict(
    parameter = 'u',
    date = 2010071000,
    latitude = {-90:90},
    longitude = {-180:179.3333},
    level = 500
)
w = reader.readArray(directive)
print("semperpy")
print(w.shape)
print(w.mean())
print()

if v.mean() != w.mean():
    raise ValueError('mean values are different')

ga('set lon 120.0 230')
ga('set lat -45 45')
v = ga.expr('u')
print("pygrads")
print(v.shape)
print(v.mean())

directive = dict(
    parameter = 'u',
    date = 2010071000,
    latitude = {-45:45},
    longitude = {120:230},
    level = 500
)
w = reader.readArray(directive)
print("semperpy")
print(w.shape)
print(w.mean())

if v.mean() != w.mean():
    raise ValueError('mean values are different')
