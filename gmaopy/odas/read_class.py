# Function read_class
#

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from numpy import *

# Define gridclass
def grid():
    
    proddir  = '/Users/claudegibert/unix/dev/p4/semperpydata/'
    gridfile = proddir + 'grid_spec.nc'
    ds       = Dataset(gridfile, 'r', format='NETCDF3')
    z        = ds.variables['zt'][:]
    x        = ds.variables['grid_x_T'][:]
    y        = ds.variables['grid_y_T'][:]
    lon      = ds.variables['x_T'][:]
    lat      = ds.variables['y_T'][:]
    mask     = ds.variables['wet'][:]
    ds.close()    
    
        class gridclass:
        pass
    grid = gridclass()
    grid.z    = z
    grid.x    = x
    grid.y    = y
    grid.lon  = lon
    grid.lat  = lat
    grid.mask = mask
    
    grid.x[grid.x<-180]=grid.x+360
    
    grid.y0 = np.where((y>=-0.1) & (y<=0.3))
    
    return grid
    

    
    



