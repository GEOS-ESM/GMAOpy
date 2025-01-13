import numpy as np
from netCDF4 import Dataset

f = Dataset('conv.ods')
kt = f.variables['kt'][:]
kt += f.variables['kt'].add_offset
kx = f.variables['kx'][:]
kx += f.variables['kx'].add_offset

kxs = kx == 289
kts = kt == 4
k = np.logical_and(kxs,kts)
v = f.variables['omf'][:]
result = v[k]
print(result.shape)
print(result.mean())
v = f.variables['obs'][:]
result = v[k]
print(result.shape)
print(result.mean())

kxs = kx == 181
kts = kt == 33
k = np.logical_and(kxs,kts)
v = f.variables['omf'][:]
result = v[k]
print(result.shape)
print(result.mean())
v = f.variables['obs'][:]
result = v[k]
print(result.shape)
print(result.mean())

f = Dataset('airs.ods')
kt = f.variables['kt'][:]
kt += f.variables['kt'].add_offset
kx = f.variables['kx'][:]
kx += f.variables['kx'].add_offset

kxs = kx == 49
kts = kt == 40
k = np.logical_and(kxs,kts)
v = f.variables['omf'][:]
result = v[k]
print(result.shape)
print(result.mean())
v = f.variables['obs'][:]
result = v[k]
print(result.shape)
print(result.mean())
