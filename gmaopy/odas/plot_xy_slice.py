#! /usr/bin/env python
# plot_xy_slice.py T   mvoi_1992_nosal -5  30 1    0  1992 1 Horizontal_Fields
# plot_xy_slice.py SSH mvoi_1992_nosal -.5 .5 0.02 0  1992 1 Horizontal_Fields


import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from netCDF4 import Dataset
from netCDF4 import MFDataset
#from numpy import *
import glob
import datetime
import string
import time
import sys
import math

from tkinter import *


#from array import *
sys.path.append('/discover/nobackup/projects/gmao/ssd/g5odas/production/GEOS5odas-3.2/rc/pproc_utils/extract_odas/')
import read_class


def find_nearest(array,value):
    idx=(np.abs(array-value)).argmin()
    return array[idx], idx


BASEDIR='/discover/nobackup/projects/gmao/ssd/g5odas/production/GEOS5odas-3.2/'

NCVAR=sys.argv[1]
EXPDIR=sys.argv[2]
expname=EXPDIR
EXPDIR=BASEDIR+EXPDIR+'/'
minval=float(sys.argv[3])
maxval=float(sys.argv[4])
stepval=float(sys.argv[5])
mom_level=int(sys.argv[6])
year=sys.argv[7]
month=sys.argv[8]
OUTDIR=sys.argv[9]

# BIAS File
# File from mvoi_test2 odas.1993010103.nc
#bias_fname = '/discover/nobackup/projects/gmao/ssd/g5odas/production/GEOS5odas-3.2/rc/pproc_utils/odas.bias.nc'
bias_fname = '/discover/nobackup/projects/gmao/ssd/g5odas/production/GEOS5odas-3.2/rc/odas/bias/bias_test.nc'

#LEVITUS STUFF
Lev_fname = '/discover/nobackup/projects/gmao/ssd/ocean/kovach/odas-2/obs/LEVITUS_GRD/levitus_grd.nc'

levels = np.arange(minval, maxval, stepval)

# Read MOM Grid File
grid = read_class.grid()

Z=grid.z[mom_level]


MONTH=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

delta=1.0
lonimin=np.minimum.reduce(np.minimum.reduce(grid.lon))
lonimax=np.maximum.reduce(np.maximum.reduce(grid.lon))+0.5

loni=np.arange(lonimin,lonimax,delta)
lati=np.arange(np.minimum.reduce(np.minimum.reduce(grid.lat)),np.maximum.reduce(np.maximum.reduce(grid.lat)),delta)

loni, lati=np.meshgrid(loni,lati)

Ni=len(loni)
Nj=len(np.transpose(loni))

loni.shape= len(loni)*len(np.transpose(loni)),1
lati.shape= len(lati)*len(np.transpose(lati)),1

timeindex=1

xticklab = ['60E','90E','120E','150E','180E','150W','120W','90W','60W','30W', '0', '30E']
xticknum = [-300, -270, -240,  -210,  -180,  -150,  -120,  -90,  -60,  -30,    0,    30]

yticklab = ['90S','60S','30S','EQ','30N','60N','90N']
yticknum = [ -90,  -60,  -30,   0,  30,   60,   90]

xlevticklab = ['60E','90E','120E','150E','180E','150W','120W','90W','60W','30W', '0', '30E']
xlevticknum = [ 60,   90,   120,   150,   180,   210,   240,   270,  300,  330,   360, 390]


tempdir=EXPDIR+'/odas/nc/*'+year+month+'*.nc'
filelist=sorted(list(glob.glob(tempdir)))

count = 0
mdata = 0

for filename in filelist:        
    year=filename[-13:-9]
    month=filename[-9:-7]
    day=filename[-7:-5]
   
    odasgrp = Dataset(filename, 'r', format='NETCDF4')
    if (NCVAR[0:3]!='SSH'):
        VAR=odasgrp.groups['fcst'].variables[NCVAR][mom_level,:,:]

    if (NCVAR[0:3]=='SSH'):
        VAR=odasgrp.groups['fcst'].variables[NCVAR][:,:]
    bias = Dataset(bias_fname, 'r', format='NETCDF4')
        #BIAS=bias.groups['bias'].variables['SSH_001'][:,:]
    BIAS=bias.variables['bias'][:,:] 
    bias.close()
        BIAS[BIAS>999]='nan'
        
    VAR[VAR>999]='nan'
    if (NCVAR[0:3]=='SSH'):
    VAR=VAR-BIAS
    clab = np.arange(-0.5,0.1,0.5)
    if (NCVAR[0]=='T'):
         clab = np.arange(-10,40,2)  
    if (NCVAR[0]=='S'):
    clab = np.arange(0,40,0.2)
    
    lon=grid.lon
    lat=grid.lat

    VAR=np.squeeze(VAR)
    lon=np.squeeze(lon)
    lat=np.squeeze(lat)

    fig = plt.figure(num=None, figsize=(12,6), facecolor='w')

    ax = plt.axes([0.05, 0.2, 0.42, 0.7])        
    if (NCVAR[0:3]!='SSH'):
        plt.title('MOM '+month+'/'+day+'/'+year+'  z='+str(grid.z[mom_level])+'m')
    if (NCVAR[0:3]=='SSH'):
        plt.title('MOM '+month+'/'+day+'/'+year+'  SLA')
    #hl   = plt.contour(lon,lat,VAR,clab,origin='lower', extend='both',colors='black')
    #hl   = plt.contour(lon-358,lat,VAR,clab,origin='lower', extend='both',colors='black')

    cim=plt.contourf(lon,lat,VAR, levels, origin='lower',cmap=cm.jet, extend='both')
    cim=plt.contourf(lon-358,lat,VAR, levels, origin='lower',cmap=cm.jet, extend='both')
    ax.axis([-340, 20, -90, 90])
    plt.xticks(xticknum,xticklab,rotation=30)
    plt.yticks(yticknum,yticklab)

    cx  = fig.add_axes([0.15, 0.075, 0.7, 0.035])
    cbar=plt.colorbar(cim,cax=cx,orientation='horizontal',extend='both')
    if (NCVAR[0]=='T'):
        cbar.ax.set_xlabel('T $[^oC]$')
    if (NCVAR[0]=='S'):
        cbar.ax.set_xlabel('S $[psu]$')        
    if (NCVAR[0:3]=='SSH'):
        cbar.ax.set_xlabel('SLA $[m]$')        

    #plt.show()
    #time.sleep(99999)
        
    # Levitus
    if ( (NCVAR[0]=='T' or NCVAR[0]=='S') and NCVAR[0:3]!='SSH' ):        
        LEV  = Dataset(Lev_fname, 'r', format='NETCDF4')
        DEPTH   = LEV.variables['DEPTH'][:]
        val, zindex = find_nearest(DEPTH,Z)
        lev_time_index=int(month)-1

        if (NCVAR[0]=='T'):
            VAR_LEV = LEV.variables['TEMP'][lev_time_index,zindex,:,:]
        if (NCVAR[0]=='S'):
            VAR_LEV = LEV.variables['SALT'][lev_time_index,zindex,:,:]

        LON   = LEV.variables['LON'][:]
        LAT   = LEV.variables['LAT'][:]

        LEV.close()
    
        ax2 = plt.axes([0.52, 0.2, 0.42, 0.7])    
    #hl  = plt.contour(LON,LAT,np.squeeze(VAR_LEV),clab,origin='lower', extend='both',colors='black')
        #hl  = plt.contour(LON+358,LAT,np.squeeze(VAR_LEV),clab,origin='lower', extend='both',colors='black')

        cim=plt.contourf(LON,LAT,np.squeeze(VAR_LEV),levels,origin='lower',cmap=cm.jet, extend='both')
        cim=plt.contourf(LON+358,LAT,np.squeeze(VAR_LEV),levels,origin='lower',cmap=cm.jet, extend='both')
        ax2.axis([20, 380, -90, 90])
        plt.title(MONTH[int(month)-1]+' Levitus')        
        plt.xticks(xlevticknum,xlevticklab,rotation=30)
        plt.yticks(yticknum,yticklab)
    # AVISO
    if (NCVAR[0:3]=='SSH' and int(year)>=1993):
    SSH_fname='/discover/nobackup/projects/gmao/ssd/ocean/kovach/odas-2/obs/AVISO_GRD/SLA_GRD_'+year+'.nc'
    SSH = Dataset(SSH_fname, 'r', format='NETCDF4')
    DATE = SSH.variables['DATE'][:]
    filedate = int(year+month+day)
        val, tindex = find_nearest(DATE,filedate)
        VAR_SSH  = SSH.variables['SSH'][tindex,:,:]    
        LON      = SSH.variables['LON'][:]
        LAT      = SSH.variables['LAT'][:]
    VAR_SSHM = SSH.variables['SSHM'][int(month)-1,:,:]
    Amonth   = SSH.variables['MON'][tindex]
    Aday     = SSH.variables['DAY'][tindex]
    Ayear    = SSH.variables['YEAR'][tindex]
    SSH.close()
        
        ax2 = plt.axes([0.52, 0.2, 0.42, 0.7])        
    #hl  = plt.contour(LON,LAT,np.squeeze(VAR_SSH),clab,origin='lower', extend='both',colors='black')
        #hl  = plt.contour(LON+358,LAT,np.squeeze(VAR_SSH),clab,origin='lower', extend='both',colors='black')
        cim=plt.contourf(LON,LAT,np.squeeze(VAR_SSH), levels, origin='lower',cmap=cm.jet, extend='both')
        cim=plt.contourf(LON+358,LAT,np.squeeze(VAR_SSH), levels, origin='lower',cmap=cm.jet, extend='both')
        ax2.axis([20, 380, -90, 90])
    plt.title('AVISO '+str(Amonth)+'/'+str(Aday)+'/'+str(Ayear))       
        plt.xticks(xlevticknum,xlevticklab,rotation=30)
        plt.yticks(yticknum,yticklab)

    if (NCVAR[0:3]=='SSH' and int(year)<1993):
    SSH_fname='/discover/nobackup/projects/gmao/ssd/ocean/kovach/odas-2/obs/AVISO_GRD/SLA_GRD_1993_1999.nc'
    SSH = Dataset(SSH_fname, 'r', format='NETCDF4')
    DATE = SSH.variables['DATE'][:]
    tindex=int(month)-1
        VAR_SSH  = SSH.variables['SSH'][tindex,:,:]    
        LON      = SSH.variables['LON'][:]
        LAT      = SSH.variables['LAT'][:]
    VAR_SSHM = SSH.variables['SSHM'][int(month)-1,:,:]
    #print VAR_SSHM[99,99]
    #time.sleep(99999)  
    Amonth   = SSH.variables['MON'][tindex]
    Aday     = SSH.variables['DAY'][tindex]
    Ayear    = SSH.variables['YEAR'][tindex]
    SSH.close()
    ax2 = plt.axes([0.52, 0.2, 0.42, 0.7])        
    #hl  = plt.contour(LON,LAT,np.squeeze(VAR_SSH),clab,origin='lower', extend='both',colors='black')
        #hl  = plt.contour(LON+358,LAT,np.squeeze(VAR_SSH),clab,origin='lower', extend='both',colors='black')
        cim=plt.contourf(LON,LAT,np.squeeze(VAR_SSH), levels, origin='lower',cmap=cm.jet, extend='both')
        cim=plt.contourf(LON+358,LAT,np.squeeze(VAR_SSH), levels, origin='lower',cmap=cm.jet, extend='both')
        ax2.axis([20, 380, -90, 90])
        #plt.title('AVISO '+str(val))     
    plt.title('AVISO '+MONTH[int(month)-1]+' Climatology (1993-1999)')       
        plt.xticks(xlevticknum,xlevticklab,rotation=30)
        plt.yticks(yticknum,yticklab)
 
    timeindex=timeindex+1

    #plt.show()
    #time.sleep(99999)

    figname=BASEDIR+expname+'/pics/'+OUTDIR+'/'+expname+'_'+year+month+day+'_'+NCVAR+'_'+str(int(Z))+'.png'
    plt.savefig(figname)
    plt.clf    
    odasgrp.close()
    
    # Add up daily data
    mdata = VAR+mdata
    count=count+1
    
######################################################################################################3
# Monthly Mean
mdata = mdata/count

fig = plt.figure(num=None, figsize=(12,6), facecolor='w')

ax = plt.axes([0.05, 0.2, 0.42, 0.7])        
if (NCVAR[0:3]!='SSH'):
        plt.title('MOM '+month+'/'+year+'  z='+str(grid.z[mom_level])+'m')
if (NCVAR[0:3]=='SSH'):
        plt.title('MOM '+month+'/'+year+'  SLA')
#hl=plt.contour(lon,lat,VAR,clab,origin='lower', extend='both',colors='black')
#hl=plt.contour(lon-358,lat,VAR,clab,origin='lower', extend='both',colors='black')
cim=plt.contourf(lon,lat,VAR, levels, origin='lower',cmap=cm.jet, extend='both')
cim=plt.contourf(lon-358,lat,VAR, levels, origin='lower',cmap=cm.jet, extend='both')
ax.axis([-340, 20, -90, 90])
plt.xticks(xticknum,xticklab,rotation=30)
plt.yticks(yticknum,yticklab)

cx  = fig.add_axes([0.15, 0.075, 0.7, 0.035])
cbar=plt.colorbar(cim,cax=cx,orientation='horizontal',extend='both')
if (NCVAR[0]=='T' and NCVAR[0:3]!='SSH'):
    cbar.ax.set_xlabel('T $[^oC]$')
if (NCVAR[0]=='S' and NCVAR[0:3]!='SSH'):
    cbar.ax.set_xlabel('S $[psu]$')        
if (NCVAR[0:3]=='SSH' and int(year)>=1993):
        cbar.ax.set_xlabel('SLA $[m]$')        

ax2 = plt.axes([0.52, 0.2, 0.42, 0.7])        
if ( (NCVAR[0]=='T' or NCVAR[0]=='S') and NCVAR[0:3]!='SSH' ):        
    #hl=plt.contour(LON,LAT,np.squeeze(VAR_LEV),clab,origin='lower', extend='both',colors='black')
        #hl=plt.contour(LON+358,LAT,np.squeeze(VAR_LEV),clab,origin='lower', extend='both',colors='black')
    cim=plt.contourf(LON,LAT,np.squeeze(VAR_LEV), levels, origin='lower',cmap=cm.jet, extend='both')
    cim=plt.contourf(LON+358,LAT,np.squeeze(VAR_LEV), levels, origin='lower',cmap=cm.jet, extend='both')
    ax2.axis([20, 380, -90, 90])
    plt.title(MONTH[int(month)-1]+' Levitus')  
if (NCVAR[0:3]=='SSH' and int(year)>=1993):    
    #hl=plt.contour(LON,LAT,np.squeeze(VAR_SSHM),clab,origin='lower', extend='both',colors='black')
        #hl=plt.contour(LON+358,LAT,np.squeeze(VAR_SSHM),clab,origin='lower', extend='both',colors='black')
        cim=plt.contourf(LON,LAT,np.squeeze(VAR_SSHM), levels, origin='lower',cmap=cm.jet, extend='both')
        cim=plt.contourf(LON+358,LAT,np.squeeze(VAR_SSHM), levels, origin='lower',cmap=cm.jet, extend='both')
    ax2.axis([20, 380, -90, 90])
    plt.title('AVISO '+month+'/'+year)     
if (NCVAR[0:3]=='SSH' and int(year)<1993):
    #hl=plt.contour(LON,LAT,np.squeeze(VAR_SSHM),clab,origin='lower', extend='both',colors='black')
        #hl=plt.contour(LON+358,LAT,np.squeeze(VAR_SSHM),clab,origin='lower', extend='both',colors='black')
        cim=plt.contourf(LON,LAT,np.squeeze(VAR_SSHM), levels, origin='lower',cmap=cm.jet, extend='both')
        cim=plt.contourf(LON+358,LAT,np.squeeze(VAR_SSHM), levels, origin='lower',cmap=cm.jet, extend='both')
    ax2.axis([20, 380, -90, 90])    
        plt.title('AVISO '+MONTH[int(month)-1]+' Climatology (1993-1999)') 
     
plt.xticks(xlevticknum,xlevticklab,rotation=30)
plt.yticks(yticknum,yticklab)

figname=BASEDIR+expname+'/pics/'+OUTDIR+'/'+expname+'_'+year+month+'_'+NCVAR+'_'+str(int(Z))+'.png'
plt.savefig(figname)
plt.clf


