from netCDF4 import Dataset
import numpy as np
from semperpy.config.configure import Configure
from semperpy.fields.netcdf.dimension import Dimension
from semperpy.fields.netcdf.filereader import FileReader
from semperpy.fields.netcdf.odasdimensions import *

class ODASFileReader(FileReader):

    grid = {}

    def createVariableMap(self,filename,file):
        variables = super(ODASFileReader,self).createVariableMap(filename,file)
        for group in list(file.groups.values()):
            for k,v in list(group.variables.items()): 
                variables[k.lower()] = v
                variables[k.upper()] = v
        if len(self.grid) == 0:
            grid = self.readGrid()
            self.grid['lev'] = grid.variables['zt'][:]
            self.grid['lat'] = grid.variables['grid_y_T'][:]
            self.grid['lon'] = grid.variables['grid_x_T'][:]
            grid.close()
            FileReader.registerDimension('lev',ODASLevel)
            FileReader.registerDimension('lat',ODASLatitude)
            FileReader.registerDimension('lon',ODASLongitude)
        for k,i in list(self.grid.items()):
            variables[k] = i
        all = filename.split('.')
        self.date_ = int(all[-2])
        return variables

    def readGrid(self):
        path = Configure.resolvePath('~/semperpydata/grid_spec.nc') 
        return Dataset(path,'r')

    def createDimension(self,dimension,variable,**kargs):
        if dimension == 'time':
            return ODASDateDimension(dimension,variable,self.date_,**kargs)
        elif dimension == 'lev':
            return ODASLevel(dimension,variable,**kargs)
        return super(ODASFileReader,self).createDimension(dimension,variable,**kargs)
