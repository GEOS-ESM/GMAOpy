#! /usr/bin/env python
#
# Extract and plot a lon/depth section  
# plot_xz_slice.py $grp $var $reg $lev[1] $lev[2] $ilat $expname $year $mon

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
import extract_xz_slice
import read_class
import get_var_info

def find_nearest(array,value):
    idx=(np.abs(array-value)).argmin()
    return array[idx], idx

def make_N_colors(cmap_name, N):
     cmap = cm.get_cmap(cmap_name, N)
     return cmap(np.arange(N))[:,:-1] 

# User Input
grp=sys.argv[1]
var=sys.argv[2]
reg=sys.argv[3]
lev=[float(sys.argv[4]),float(sys.argv[5])]
ilat=float(sys.argv[6])
expname=sys.argv[7]
year=sys.argv[8]
month=sys.argv[9]
#

BASEDIR='/discover/nobackup/projects/gmao/ssd/g5odas/production/GEOS5odas-3.2/'
EXPDIR=BASEDIR+expname+'/'
OUTDIR=EXPDIR+'pics/Vertical_Fields/xz_slice/'
    
zticklab = ['0','100','200','300','400','500','600','700','800','900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','2000']
zticknum = [0,-100,-200,-300,-400,-500,-600,-700,-800,-900,-1000,-1100,-1200,-1300,-1400,-1500,-1600,-1700,-1800,-1900,-2000]

if lev[1] > 500:
    zticklab = ['0','200','400','600','800','1000','1200','1400','1600','1800','2000']
    zticknum = [0,-200,-400,-600,-800,-1000,-1200,-1400,-1600,-1800,-2000]
    
# Get Variable Info
var_info = get_var_info.var_info(var)
cmap  = make_N_colors('jet',len(var_info.datarange))

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
    ext = extract_xz_slice.ext(filename,grp,var,lev,reg,ilat)
    
    # Plot MOM Field
    fig = plt.figure(num=None, figsize=(8,10), facecolor='w')
    
    ax1 = plt.axes([0.1, 0.71, 0.75, 0.25])
    plt.title('MOM '+month+'/'+day+'/'+year+' '+ext.longname)
    if (reg=='glb'):
        plt.title('MOM '+month+'/'+day+'/'+year+' '+ext.longname+' Lat='+str(ilat))
    hl   = plt.contour(ext.lon,-ext.z,ext.data,var_info.contours,origin='lower', extend='both',colors='black',linewidths=var_info.clabfat)
    #plt.clabel(hl,var_info.clab,fmt='%2.1f',inlinespacing=1,rightside_up='true')
    hf   = plt.contourf(ext.lon,-ext.z,ext.data,var_info.datarange,origin='lower', extend='both',colors=cmap)
    
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
    LON            = LEV.variables['LON'][:]
    LAT            = LEV.variables['LAT'][:]
    yval, yindex   = find_nearest(LAT,0)
    LEV_Y = yval
    if (reg=='eqpac'):
        ix = ((LON>=135) & (LON<=265))
        xx = np.where(ix)
        VAR_LEV = LEV.variables[var_info.lev_var][lev_time_index,0:zindex,yindex,xx[0]]    
        LEV_X   = LON[xx]
    if (reg=='eqind'):
        ix = ((LON>=44) & (LON<=96))
        xx = np.where(ix)
        VAR_LEV = LEV.variables[var_info.lev_var][lev_time_index,0:zindex,yindex,xx[0]]    
        LEV_X   = LON[xx]
    if (reg=='eqatl'):
        xx1  = where(LON>=315)
        lon1 = LON[xx1]
        xx2  = where(LON<=10)
        lon2 = LON[xx2]
        xx = [concatenate((xx1,xx2),axis=1)]
        lon = squeeze(LON[xx])
        xx      = xx[0][0]
        x360 = np.where(lon>180)
        lon[x360]=lon[x360]-360
        VAR_LEV = LEV.variables[var_info.lev_var][lev_time_index,0:zindex,yindex,xx]
        LEV_X   = lon
    if (reg=='glb'):
        xx1  = where(LON>=20)
        lon1 = LON[xx1]
        xx2  = where(LON<20)
        lon2 = LON[xx2]
        xx = [concatenate((xx1,xx2),axis=1)]
        xx      = xx[0][0]    
        lon = squeeze(LON[xx])
        xlon, ix = find_nearest(lon,360)
        lon[ix+1:] = lon[ix+1:]+360
        LEV_X = lon
        yval, yindex   = find_nearest(LAT,ilat)
        LEV_Y = yval
        VAR_LEV = LEV.variables[var_info.lev_var][lev_time_index,0:zindex,yindex,xx]    
        
    LEV_Z   = DEPTH[0:zindex]
    LEV.close()
        
    ax2 = plt.axes([0.1, 0.41, 0.75, 0.25])
    plt.title(MONTH[int(month)-1]+' Levitus')        
    hl   = plt.contour(LEV_X,-LEV_Z,VAR_LEV,var_info.contours,origin='lower', extend='both',colors='black',linewidths=var_info.clabfat)
    #plt.clabel(hl,var_info.clab,fmt='%2.1f',inlinespacing=1,rightside_up='true')
    hf   = plt.contourf(LEV_X,-LEV_Z,VAR_LEV,var_info.datarange,origin='lower', extend='both',colors=cmap)
    ax2.axis([ext.axis[0], ext.axis[1], -lev[1], lev[0]])
    plt.xticks(ext.xticknum,ext.xticklab)
    plt.yticks(zticknum,zticklab)
    plt.ylim(-lev[1],lev[0])
    
    figname=OUTDIR+'/'+expname+'_'+year+month+day+'_'+var+'_'+reg+'_'+str(int(lev[0]))+'_'+str(int(lev[1]))+'.png'
    #figname='test1.png'
        
    plt.savefig(figname)
    plt.clf
    
    # Add up daily data
    mdata = ext.data+mdata
    timeindex=timeindex+1

    
######################################################################################################3
# Monthly Mean
mdata = mdata/timeindex

# ARGO Monthly Mean
if (reg=='eqpac' and  year>='2002' and year <='2009' and lev[1]<=500):    
    arg_fname      = '/discover/nobackup/projects/gmao/ssd/ocean/kovach/odas-2/obs/ARGO_GRD/ARGO_'+year+'_eqpac.nc'
    arg_time_index = int(month)-1
    ARG            = Dataset(arg_fname, 'r', format='NETCDF4')
    ARG_ZT         = ARG.variables['ZT'][arg_time_index,:]
    ARG_XT         = ARG.variables['XT'][arg_time_index,:]
    ARG_Y          = ARG.variables['LAT'][:]
    ARG_ZS         = ARG.variables['ZS'][arg_time_index,:]
    ARG_XS         = ARG.variables['XS'][arg_time_index,:]
    VAR_ARG        = (ARG.variables[var_info.lev_var][arg_time_index,:])    
    ARG.close()
    ARG_X = ARG_XT
    ARG_Z = ARG_ZT
    if (var_info.name=='S'):
        ARG_X = ARG_XS
        ARG_Z = ARG_ZS

fig = plt.figure(num=None, figsize=(8,10), facecolor='w')

ax1 = plt.axes([0.1, 0.71, 0.75, 0.25])
plt.title('MOM '+month+'/'+year+' '+ext.longname)
if (reg=='glb'):
    plt.title('MOM '+month+'/'+year+' '+ext.longname+' Lat='+str(ilat))
    
hl   = plt.contour(ext.lon,-ext.z,mdata,var_info.contours,origin='lower', extend='both',colors='black',linewidths=var_info.clabfat)
#plt.clabel(hl,var_info.clab,fmt='%2.1f',inlinespacing=1,rightside_up='true')
hf   = plt.contourf(ext.lon,-ext.z,mdata,var_info.datarange,origin='lower', extend='both',colors=cmap)


if (reg=='eqpac' and  year>='2002' and year <='2009' and lev[1]<=500):    
    for i in range(len(ARG_X)):
        delta = min(diff(var_info.datarange))
        #print i, delta,VAR_ARG[i], min(var_info.datarange)
        cinc  = floor((VAR_ARG[i]-min(var_info.datarange))/delta);        
        if (cinc<0):
            cinc=0
        if cinc>cmap.shape[0]: 
            cinc=cmap.shape[0]
        hl=plt.plot(ARG_X[i],-ARG_Z[i],marker='o',color=cmap[cinc,:],markersize=5)

plt.xticks(ext.xticknum,ext.xticklab)
plt.yticks(zticknum,zticklab)
plt.ylim(-lev[1],lev[0])
ax1.axis([ext.axis[0], ext.axis[1], -lev[1], lev[0]])

coloraxis_2 = [0.9, 0.47, 0.025, 0.45]
coloraxis_3 = [0.9, 0.2,  0.025, 0.68]

coloraxis = coloraxis_2
if (reg=='eqpac' and  year>='1993' and lev[1]<=500):
    coloraxis = coloraxis_3
if (reg=='eqatl' and  year>='2000' and lev[1]<=500):
    coloraxis = coloraxis_3

cx = fig.add_axes(coloraxis)
cbar=plt.colorbar(hf,cax=cx,orientation='vertical',extend='both')
cbar.ax.set_xlabel(var_info.units)

# Levitus Climatology
ptitle = 'Levitus'
ax2 = plt.axes([0.1, 0.41, 0.75, 0.25])
plt.title(MONTH[int(month)-1]+' '+ptitle)        
hl   = plt.contour(LEV_X,-LEV_Z,VAR_LEV,var_info.contours,origin='lower', extend='both',colors='black',linewidths=var_info.clabfat)
hf   = plt.contourf(LEV_X,-LEV_Z,VAR_LEV,var_info.datarange,origin='lower', extend='both',colors=cmap)
ax2.axis([ext.axis[0], ext.axis[1], -lev[1], lev[0]])
plt.xticks(ext.xticknum,ext.xticklab)
plt.yticks(zticknum,zticklab)
plt.ylim(-lev[1],lev[0])

# TAO Monthly Mean
if (reg=='eqpac' and  year>='1993' and lev[1]<=500):
    lev_fname      = '/discover/nobackup/projects/gmao/ssd/ocean/kovach/odas-2/obs/TAO_GRD/TAO_'+year+'_eqpac.nc'
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
    hl   = plt.contour(LEV_X,-LEV_Z,VAR_LEV,var_info.contours,origin='lower', extend='both',colors='black',linewidths=var_info.clabfat)
    hf   = plt.contourf(LEV_X,-LEV_Z,VAR_LEV,var_info.datarange,origin='lower', extend='both',colors=cmap)
    hpos = plt.plot(LEV_Xpos,LEV_Zpos,'kx')
    ax3.axis([ext.axis[0], ext.axis[1], -lev[1], lev[0]])
    plt.xticks(ext.xticknum,ext.xticklab)
    plt.yticks(zticknum,zticklab)
    plt.ylim(-lev[1],lev[0])
    
# PIR Monthly Mean
if (reg=='eqatl' and  year>='2000' and lev[1]<=500):
    lev_fname      = '/discover/nobackup/projects/gmao/ssd/ocean/kovach/odas-2/obs/PIR_GRD/PIR_'+year+'_eqatl.nc'
    LEV            = Dataset(lev_fname, 'r', format='NETCDF4')
    LEV_Z          = LEV.variables['DEPTH'][:]
    LEV_X          = LEV.variables['LON'][:]
    LEV_Y          = LEV.variables['LAT'][:]
    LEV_Xpos       = LEV.variables[var+'X'][:]
    LEV_Zpos       = LEV.variables[var+'Z'][:]
    VAR_LEV        = (LEV.variables[var_info.lev_var][lev_time_index,:,:])    
    LEV.close()
    ptitle = year+' PIRATA'        
    ax3 = plt.axes([0.1, 0.11, 0.75, 0.25])
    plt.title(MONTH[int(month)-1]+' '+ptitle)        
    hl   = plt.contour(LEV_X,-LEV_Z,VAR_LEV,var_info.contours,origin='lower', extend='both',colors='black',linewidths=var_info.clabfat)
    hf   = plt.contourf(LEV_X,-LEV_Z,VAR_LEV,var_info.datarange,origin='lower', extend='both',colors=cmap)
    hpos = plt.plot(LEV_Xpos,LEV_Zpos,'kx')
    ax3.axis([ext.axis[0], ext.axis[1], -lev[1], lev[0]])
    plt.xticks(ext.xticknum,ext.xticklab)
    plt.yticks(zticknum,zticklab)
    plt.ylim(-lev[1],lev[0])

figname=OUTDIR+'/'+expname+'_'+year+month+'_'+var+'_'+reg+'_'+str(int(lev[0]))+'_'+str(int(lev[1]))+'.png'
#figname='test2.png'
plt.savefig(figname)
plt.clf
    
