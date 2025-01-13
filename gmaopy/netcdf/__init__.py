from semperpy.netcdf.file import File
from semperpy.slicing.cf10.latdimension import LatDimension
from semperpy.slicing.cf10.londimension import LonDimension
from semperpy.slicing.cf10.datedimension import DateDimension
from semperpy.slicing.cf10.leveldimension import LevelDimension

File.registerDimension('lat','latitude',LatDimension)
File.registerDimension('latitude','latitude',LatDimension)
File.registerDimension('YDim:EOSGRID','latitude',LatDimension)
File.registerDimension('lon','longitude',LonDimension)
File.registerDimension('longitude','longitude',LonDimension)
File.registerDimension('XDim:EOSGRID','longitude',LonDimension)
File.registerDimension('time','date',DateDimension)
File.registerDimension('TIME:EOSGRID','date',DateDimension)
File.registerDimension('lev','level',LevelDimension)
File.registerDimension('levels','level',LevelDimension)
File.registerDimension('Height:EOSGRID','level',LevelDimension)
