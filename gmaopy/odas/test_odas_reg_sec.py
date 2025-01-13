#! /usr/bin/env python
#
# Extract and plot a section plot for (lon/lat,depth) region

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from numpy import *
import extract_odas_reg_sec

# User Input
fname = 'odas.1992050103.nc'
grp   = 'fcst'
var   = 'T_002'       
lev   = [0, 500]      # depth range
reg   = 'eqpac'       # eqpac, eqind, eqatl
#


# returns ext structure of lat, lon, z, data
ext = extract_odas_reg_sec.ext(fname,grp,var,lev,reg)
print(shape(ext.data))
print(shape(ext.z))

levels = np.arange(4,32,1)
fig = plt.figure()
ax  = fig.add_subplot(111)
#plt.contourf(ext.data[ ::-1,:],levels)
h   = plt.contourf(ext.lon,-ext.z,ext.data,levels,origin='lower', extend='both')
ax.axis('tight')
cbar=plt.colorbar(h,orientation='horizontal',shrink=0.8, extend='both')
plt.show()    
