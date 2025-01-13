#! /usr/bin/env python
#
# Extract and plot a lon/depth section 
# plot_yz_slice.py $grp $var $reg $lev[1] $lev[2] $expname $year $mon

import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from netCDF4 import Dataset
from netCDF4 import MFDataset
from numpy import *
import glob
import datetime
import string
import time
import sys
import math
from tkinter import *

import array
sys.path.append('/discover/nobackup/projects/gmao/ssd/g5odas/production/GEOS5odas-3.2/rc/pproc_utils/extract_odas/')
import extract_yz_slice
import read_class
import get_var_info

def find_nearest(array,value):
    idx=(np.abs(array-value)).argmin()
    return array[idx], idx

# User Input
grp=sys.argv[1]
var=sys.argv[2]
reg=sys.argv[3]
lev=[float(sys.argv[4]),float(sys.argv[5])]
expname=sys.argv[6]
year=sys.argv[7]
month=sys.argv[8]
#

BASEDIR='/discover/nobackup/projects/gmao/ssd/g5odas/production/GEOS5odas-3.2/'
EXPDIR=BASEDIR+expname+'/'
OUTDIR=EXPDIR+'pics/Vertical_Fields/yz_slice/'

zticklab = ['0','100','200','300','400','500','600','700','800','900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','2000']
zticknum = [0,-100,-200,-300,-400,-500,-600,-700,-800,-900,-1000,-1100,-1200,-1300,-1400,-1500,-1600,-1700,-1800,-1900,-2000]

if lev[1] > 500:
    zticklab = ['0','200','400','600','800','1000','1200','1400','1600','1800','2000']
    zticknum = [0,-200,-400,-600,-800,-1000,-1200,-1400,-1600,-1800,-2000]
    
# Get Variable Info
var_info = get_var_info.var_info(var)

# Loop through one month
tempdir=EXPDIR+'/odas/nc/*'+year+month+'*.nc'
filelist=sorted(list(glob.glob(tempdir)))

timeindex=0
mdata=0

for filename in filelist:        
    year=filename[-13:-9]
    month=filename[-9:-7]
    day=filename[-7:-5]
    
    # Extract Data (ext structure of lat, lon, z, data)
    ext = extract_yz_slice.ext(filename,grp,var,lev,reg)
    
    # Plot MOM Field
    fig = plt.figure(num=None, figsize=(8,10), facecolor='w')
    
    ax1 = plt.axes([0.1, 0.71, 0.75, 0.25])
    plt.title('MOM '+month+'/'+day+'/'+year+' '+ext.longname)
    hl   = plt.contour(ext.lat,-ext.z,ext.data,var_info.contours,origin='lower', extend='both',colors='black',linewidths=var_info.clabfat)
        #plt.clabel(hl,var_info.clab,fmt='%2.1f',inlinespacing=1,rightside_up='true')
    hf   = plt.contourf(ext.lat,-ext.z,ext.data,var_info.datarange,origin='lower', extend='both',cmap=cm.jet)
    
    plt.xticks(ext.xticknum,ext.xticklab)
    plt.yticks(zticknum,zticklab)
    plt.ylim(-lev[1],lev[0])
    ax1.axis([ext.axis[0], ext.axis[1], -lev[1], lev[0]])
    cx  = fig.add_axes([0.9, 0.47, 0.025, 0.45])
    cbar=plt.colorbar(hf,cax=cx,orientation='vertical',extend='both')
    cbar.ax.set_xlabel(var_info.units)
        
    # Levitus Climatology
    lev_fname      = '/discover/nobackup/projects/gmao/ssd/ocean/kovach/odas-2/obs/LEVITUS_GRD/levitus_grd.nc'
    MONTH          = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    lev_time_index = int(month)-1
    LEV            = Dataset(lev_fname, 'r', format='NETCDF4')
    DEPTH          = LEV.variables['DEPTH'][:]
    zval, zindex   = find_nearest(DEPTH,max(ext.z))
    LEV_Z          = DEPTH[0:zindex]
    LON            = LEV.variables['LON'][:]
    LAT            = LEV.variables['LAT'][:]
    LEV_X, xindex  = find_nearest(LON,ext.lon)
    if (ext.lon<0):
        LEV_X, xindex  = find_nearest(LON,ext.lon+360)    
    
    iy             = ((LAT>=ext.lat[0]) & (LAT<=ext.lat[-1]))
    yy             = np.where(iy)
    VAR_LEV        = LEV.variables[var_info.lev_var][lev_time_index,0:zindex,yy[0],xindex]    
    LEV_Y          = LAT[yy]
    LEV.close()
    
    ax2 = plt.axes([0.1, 0.12, 0.75, 0.35])
    plt.title(MONTH[int(month)-1]+' Levitus')        
    hl   = plt.contour(LEV_Y,-LEV_Z,VAR_LEV,var_info.contours,origin='lower', extend='both',colors='black',linewidths=var_info.clabfat)
        #plt.clabel(hl,var_info.clab,fmt='%2.1f',inlinespacing=1,rightside_up='true')
    hf   = plt.contourf(LEV_Y,-LEV_Z,VAR_LEV,var_info.datarange,origin='lower', extend='both',cmap=cm.jet)
    ax2.axis([ext.axis[0], ext.axis[1], -lev[1], lev[0]])
    plt.xticks(ext.xticknum,ext.xticklab)
    plt.yticks(zticknum,zticklab)
    plt.ylim(-lev[1],lev[0])
    
    figname=OUTDIR+'/'+expname+'_'+year+month+day+'_'+var+'_'+reg+'_'+str(int(lev[0]))+'_'+str(int(lev[1]))+'.png'

    plt.savefig(figname)
    plt.clf
    
    # Add up daily data
    mdata = ext.data+mdata
    timeindex=timeindex+1

######################################################################################################3
# Monthly Mean
mdata = mdata/timeindex
fig = plt.figure(num=None, figsize=(8,10), facecolor='w')

ax1 = plt.axes([0.1, 0.71, 0.75, 0.25])
plt.title('MOM '+month+'/'+year+' '+ext.longname)
hl   = plt.contour(ext.lat,-ext.z,ext.data,var_info.contours,origin='lower', extend='both',colors='black',linewidths=var_info.clabfat)
#plt.clabel(hl,var_info.clab,fmt='%2.1f',inlinespacing=1,rightside_up='true')
hf   = plt.contourf(ext.lat,-ext.z,ext.data,var_info.datarange,origin='lower', extend='both',cmap=cm.jet)

plt.xticks(ext.xticknum,ext.xticklab)
plt.yticks(zticknum,zticklab)
plt.ylim(-lev[1],lev[0])
ax1.axis([ext.axis[0], ext.axis[1], -lev[1], lev[0]])
if (reg[0]=='p' and  year>='1993' and lev[1]<=500):
    cx  = fig.add_axes([0.9, 0.2, 0.025, 0.68])
else:
    cx  = fig.add_axes([0.9, 0.47, 0.025, 0.45])
cbar=plt.colorbar(hf,cax=cx,orientation='vertical',extend='both')
cbar.ax.set_xlabel(var_info.units)

ptitle = 'Levitus'
ax2 = plt.axes([0.1, 0.41, 0.75, 0.25])
plt.title(MONTH[int(month)-1]+' '+ptitle)        
hl   = plt.contour(LEV_Y,-LEV_Z,VAR_LEV,var_info.contours,origin='lower', extend='both',colors='black',linewidths=var_info.clabfat)
#plt.clabel(hl,var_info.clab,fmt='%2.1f',inlinespacing=1,rightside_up='true')
hf   = plt.contourf(LEV_Y,-LEV_Z,VAR_LEV,var_info.datarange,origin='lower', extend='both',cmap=cm.jet)
ax2.axis([ext.axis[0], ext.axis[1], -lev[1], lev[0]])
plt.xticks(ext.xticknum,ext.xticklab)
plt.yticks(zticknum,zticklab)
plt.ylim(-lev[1],lev[0])

# TAO Monthly Mean
if (reg[0]=='p' and year>='1993' and lev[1]<=500):            
    lev_fname      = '/discover/nobackup/projects/gmao/ssd/ocean/kovach/odas-2/obs/TAO_GRD/TAO_'+year+'_'+reg+'.nc'
    MONTH          = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    lev_time_index = int(month)-1
    LEV            = Dataset(lev_fname, 'r', format='NETCDF4')
    LEV_Z          = LEV.variables['DEPTH'][:]
    LEV_X          = LEV.variables['LON'][:]
    LEV_Y          = LEV.variables['LAT'][:]
    LEV_Xpos       = LEV.variables[var+'X'][:]
    LEV_Zpos       = LEV.variables[var+'Z'][:]
    VAR_LEV        = (LEV.variables[var_info.lev_var][lev_time_index,:,:])    
    LEV.close()
    ptitle = year+' TAO'            
    ax3 = plt.axes([0.1, 0.11, 0.75, 0.25])
    plt.title(MONTH[int(month)-1]+' '+ptitle)        
    hl   = plt.contour(LEV_Y,-LEV_Z,VAR_LEV,var_info.contours,origin='lower', extend='both',colors='black',linewidths=var_info.clabfat)
    hf   = plt.contourf(LEV_Y,-LEV_Z,VAR_LEV,var_info.datarange,origin='lower', extend='both',cmap=cm.jet)
    hpos = plt.plot(LEV_Xpos,LEV_Zpos,'kx')
    ax1.axis([ext.axis[0], ext.axis[1], -lev[1], lev[0]])
    plt.xticks(ext.xticknum,ext.xticklab)
    plt.yticks(zticknum,zticklab)
    plt.ylim(-lev[1],lev[0])

figname=OUTDIR+'/'+expname+'_'+year+month+'_'+var+'_'+reg+'_'+str(int(lev[0]))+'_'+str(int(lev[1]))+'.png'
plt.savefig(figname)
plt.clf
    
