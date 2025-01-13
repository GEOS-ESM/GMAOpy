#! /usr/bin/env python
#
# array.shape=i,j

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from numpy import *
import read_class
import time

def find_nearest(array,value):
    idx=(np.abs(array-value)).argmin()
    return array[idx], idx

def ext(fname,grp,var,lev,reg):
    
    class extractclass:
        pass
    ext   = extractclass()
    
    # Read MOM Grid File
    grid = read_class.grid()

    # Define regionclass
    class region(object):
        def _init_(self, name=None):
            self.name = name
            self.lat  = lat
            self.lon  = lon
        
    p165E=region()
    p165E.name='p165E'
    p165E.longname='165E'
    p165E.lon=[165]

    p180E=region()
    p180E.name='p180E'
    p180E.longname='180E'
    p180E.lon=[180]
    
    p155W=region()
    p155W.name='p155W'
    p155W.longname='155W'
    p155W.lon=[-155]
    
    p140W=region()
    p140W.name='p140W'
    p140W.longname='140W'
    p140W.lon=[-140]
    
    p125W=region()
    p125W.name='p125W'
    p125W.longname='125W'
    p125W.lon=[-125]
    
    p110W=region()
    p110W.name='p110W'
    p110W.longname='110W'
    p110W.lon=[-110]
    
    a30W=region()
    a30W.name='a30W'
    a30W.longname='30W'
    a30W.lon=[-30]
    
    a15W=region()
    a15W.name='a15W'
    a15W.longname='15W'
    a15W.lon=[-15]
    
    i60E=region()
    i60E.name='i60E'
    i60E.longname='60E'
    i60E.lon=[60]
    
    i75E=region()
    i75E.name='i75E'
    i75E.longname='75E'
    i75E.lon=[75]
    
    i90E=region()
    i90E.name='i90E'
    i90E.longname='90E'
    i90E.lon=[90]
    
    for region in [eval(reg)]:
        lon          = region.lon
        ext.longname = region.longname
        lat          = [-30,30]
        ext.axis     = [-25,25]
        ext.xticklab = ['25S','20S','15S','10S','5S','Eq','5N','10N','15N','20N','25N']
        ext.xticknum = [-25,-20,-15,-10,-5,0,5,10,15,20,25]
        
    
    miss = 99999
    
    # Read Dataset
    ds   = Dataset(fname, 'r', format='NETCDF4')
    #time = ds.variables['time'][:]
    
    # Extract Dataset
    iz    = ((grid.z>=lev[0]) & (grid.z<=lev[1]))
    zz    = np.where(iz)
    zz    = append(zz[0],max(zz[0])+1)
    ext.z = grid.z[zz]
    
    ext.lon     = lon
    ext.lon, ix = find_nearest(grid.x,lon)
    
    iy = ((grid.y>=lat[0]) & (grid.y<=lat[1]))
    yy = np.where(iy)
    ext.lat = grid.y[yy]
    
    ext.data    = squeeze(ds.groups[grp].variables[var][zz,yy[0],ix])
    print(zz)
    print(yy[0])
    print(ix)
    ext.data[abs(ext.data)>miss]=nan
                            
    #print 'MOM: ',ext.lon
        
    ds.close()
    return ext
