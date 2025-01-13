#! /usr/bin/env python
#
# Extract and plot a surface region (lon,lat) at any chosen model level

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from numpy import *
import extract_odas_reg_sfc

# User Input
fname = 'odas.2000063003.nc'
grp   = 'fcst'
var   = 'T'       
lev   = 1             # model level
reg   = 'eqpac'       # eqpac, eqind, eqatl
#


# returns ext structure of lat, lon, z, data
ext = extract_odas_reg_sfc.ext(fname,grp,var,lev,reg)

print(ext)
