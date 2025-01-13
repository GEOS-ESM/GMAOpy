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

def ext(fname,grp,var,lev,reg,ilat):
    
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
        
    eqpac=region()
    eqpac.name='eqpac'
    eqpac.longname='Eq Pac'
    eqpac.lat=grid.y[grid.y0]
    eqpac.lon=[135,-95]
    eqpac.axis=[140, 260]
    eqpac.xticklab = ['145E','160E','180E','160W','140W','120W','95W']
    eqpac.xticknum = [145,    160,   180,   200,   220,   240,  255]

    eqind=region()
    eqind.name='eqind'
    eqind.longname='Eq Ind'
    eqind.lat=grid.y[grid.y0]
    eqind.lon=[44, 96]
    eqind.axis=[45, 95]
    eqind.xticklab = ['50E','55E','60E','65E','70E','75E','80E','85E','90E','95E']
    eqind.xticknum = [ 50,   55,   60,   65,   70,   75,   80,   85,   90,   95]

    eqatl=region()
    eqatl.name='eqatl'
    eqatl.longname='Eq Atl'
    eqatl.lat=grid.y[grid.y0]
    eqatl.lon=[-44,6]
    eqatl.axis=[-40,5]
    eqatl.xticklab = ['40W','35W','30W','25W','20W','15W','10W','5W','0','5E']
    eqatl.xticknum = [-40, -35,  -30,  -25,  -20,  -15,  -10,  -5,   0,   5]
    
    glb=region()
    glb.name='glb'
    glb.longname='Global'
    glb.lat=grid.y[:]
    glb.lon=grid.x[:]
    glb.axis=[20,380]
    glb.xticklab = ['30E','60E','90E','120E','150E','180E','150W','120W','90W','60W','30W', '0']
    glb.xticknum = [ 30,   60,   90,   120,   150,   180,   210,   240,   270,  300,  330,   360]

    
    for region in [eval(reg)]:
        lat          = region.lat
        lon          = region.lon
        ext.xticklab = region.xticklab
        ext.xticknum = region.xticknum
        ext.longname = region.longname
        ext.axis     = region.axis
        
    
    miss = 99999
    
    # Read Dataset
    ds   = Dataset(fname, 'r', format='NETCDF4')
    #time = ds.variables['time'][:]
    
    # Extract Dataset
    iz = ((grid.z>=lev[0]) & (grid.z<=lev[1]))
    zz = np.where(iz)
    zz = append(zz[0],max(zz[0])+1)
    ext.z = grid.z[zz]
    print('zz',zz)

    if (reg=='glb'):
        ext.lat, iy = find_nearest(grid.y,ilat)
        ext.lon     = lon
        xx1         = np.where((grid.x>=20) & (grid.x<=grid.x[719]))
        xx2         = [np.arange(0, xx1[0][0], 1)]            
        xx          = [concatenate((xx1,xx2),axis=1)]
        ext.lon     = squeeze(grid.x[xx])
        xx          = xx[0][0]
        data        = squeeze(ds.groups[grp].variables[var][zz,iy,:])
        data[abs(data)>miss]='nan'
        ext.data = data[:][:,xx]
        x360 = np.where(ext.lon<0)
        ext.lon[x360]=ext.lon[x360]+360
        xlon, ix = find_nearest(ext.lon,360)
        ext.lon[ix+1:] = ext.lon[ix+1:]+360


    if size(lat)==1:
        ext.lat = lat
        ix = ((grid.x>=lon[0]) & (grid.x<=lon[1]))
        xx = np.where(ix)
        if (reg=='eqind'):
            #print 'Crosses 80 Longitude'
            ishift  = np.min(where(grid.x>=0))
            xx1     = np.where((grid.x>=lon[0]) & (grid.x<=grid.x[719]))    
            xx2     = np.where((grid.x<=lon[1]) & (grid.x>grid.x[719]))            
            xx      = [concatenate((xx1,xx2),axis=1)]
                ext.lon = squeeze(grid.x[xx])
            xx      = xx[0][0]
            data    = squeeze(ds.groups[grp].variables[var][zz,min(grid.y0),:])
            data[abs(data)>miss]=nan
            ext.data = data[:][:,xx]
            print('yy',min(grid.y0),xx)
            print('xx',xx)
            
        if (reg=='eqatl'):    
            ext.data = squeeze(ds.groups[grp].variables[var][zz,min(grid.y0),xx[0]])
            ext.data[abs(ext.data)>miss]=nan
            ext.lon = grid.x[xx]
            print('yy',min(grid.y0))
            print('xx',xx)
            
        if (reg=='eqpac'):
            xx1  = where(grid.x>=lon[0])
            lon1 = grid.x[xx1]
            xx2  = where(grid.x<=lon[1])
            lon2 = grid.x[xx2]
            xx = [concatenate((xx1,xx2),axis=1)]
            ext.lon = squeeze(grid.x[xx])
            xx      = xx[0][0]
            data    = squeeze(ds.groups[grp].variables[var][zz,min(grid.y0),:])
            print('yy',min(grid.y0))
            print('xx',xx)
            data[abs(data)>miss]=nan
            ext.data = data[:][:,xx]
            x360 = np.where(ext.lon<0)
            ext.lon[x360]=360+ext.lon[x360]
    ds.close()
    return ext
