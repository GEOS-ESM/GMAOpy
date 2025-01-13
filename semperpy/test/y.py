import numpy as np
from netCDF4 import Dataset

for i in range(1):
    f = Dataset('conv.ods')
    kt = np.array(f.variables['kt'][:])
    kt += f.variables['kt'].add_offset
    kx = np.array(f.variables['kx'][:])
    kx += f.variables['kx'].add_offset

    kxs = kx == 289
    kts = kt == 4
    k = np.logical_and(kxs,kts)
    v = np.array(f.variables['omf'][:])
    result = v[k]
    v = np.array(f.variables['obs'][:])
    result = v[k]
