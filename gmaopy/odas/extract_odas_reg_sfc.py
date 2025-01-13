#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from numpy import *
import read_class

def ext(fname,grp,var,lev,reg):

    # Define regionclass
    class region(object):
        def _init_(self, name=None):
            self.name = name
            self.lat  = lat
            self.lon  = lon
        
    eqpac=region()
    eqpac.name='eqpac'
    eqpac.lat=[-30,30]
    eqpac.lon=[-240, -89]

    eqind=region()
    eqind.name='eqind'
    eqind.lat=[-30,30]
    eqind.lon=[45, 95]

    eqatl=region()
    eqatl.name='eqatl'
    eqatl.lat=[-30,30]
    eqatl.lon=[-40,0]
    
    for region in [eval(reg)]:
        lat = region.lat
        lon = region.lon
    
    miss = 99999

    # Read MOM Grid File
    grid = read_class.grid()

    # Read Dataset
    ds   = Dataset(fname, 'r', format='NETCDF4')
    data = ds.groups[grp].variables[var][:,:,:]
    data[abs(data)>miss]=nan
    time = ds.variables['time'][:]
    #print time


    class extractclass:
        pass
    ext   = extractclass()

    xyrange = (grid.lat>=lat[0]) & (grid.lat<=lat[1]) & (grid.lon>=lon[0]) & (grid.lon<=lon[1])
    i  = np.where(xyrange)
    im = max(i[0])-min(i[0])
    jm = max(i[1])-min(i[1])
    
    ext.data = data[lev-1,i[0],i[1]]
    ext.data = reshape(ext.data,[im+1,jm+1])
    ext.lat  = grid.lat[i[0],i[1]]
    ext.lat  = reshape(ext.lat,[im+1,jm+1])
    ext.lon  = grid.lon[i[0],i[1]]
    ext.lon  = reshape(ext.lon,[im+1,jm+1])
    ext.z    = grid.z[lev-1]
        
    return ext
