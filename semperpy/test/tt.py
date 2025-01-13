from semperpy.language.validate import validateChoice
from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.fields.netcdf.file import File
from pylab import *
from grads import GrADS
from pylab import prctile

#   Start GrADS and open the data file
#   ----------------------------------
ga = GrADS(Echo=False,Window=False) # quiet as a mouse
fh = ga.open('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM')
r = File('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM',GMAOConfig(ignore_missing=True,verbose=10,use_intervals=False))

#   XY slices
#   ---------
ga('set time 0Z5feb2003 21Z5feb2003') # 1 day worth of data
ga('set lon -179.375 179.375')
ga('set lat -90 90')
gslp = ga.expr('slp')/100.0-1000.0

directive = dict(
    parameter = 'SLP',
    date = [2003020500,2003020521],
)
slp = r[directive] / 100.0 - 1000.0
print(slp.shape,gslp.shape)
print(slp.mean(), gslp.mean())
print(slp.std(), gslp.std())

#   XYT slices with lat/lon subsetting
#   ----------------------------------
ga('set lon -140 -40') # restrict longitude to [140W,40W]
ga('set lat 20 50')    # restrict latitude  to [20N,50N] 
ga('set time 0Z5feb2003 21Z5feb2003') # 1 day worth of data
gslp = ga.expr('slp')/100.0-1000.0

directive = dict(
    parameter = 'slp',
    date = [2003020500,2003020521],
    lon = [-140,-40],
    lat = [20,50]
)
slp = r[directive] / 100.0 - 1000.0
print(slp.shape,gslp.shape)
print(slp.mean(), gslp.mean())
print(slp.std(), gslp.std())

#   XYZ slices
#   ----------
ga('set time 12Z13nov2003')  # Jonas' birthday
ga('set lev 300 200')        # range of levels
gspeed = ga.expr('mag(u,v)')  # mag() is grads function for wind speed

directive = dict(
    parameter = 'u',
    level = [300,200],
    date = [2003111312],
    lon = [-140,-40],
    lat = [20,50]
)

u = r[directive]
directive['parameter'] = 'v'
v = r[directive]
speed = u * u + v * v
speed = sqrt(speed)
print(speed.shape,gspeed.shape)
print(speed.mean(), gspeed.mean())
print(speed.std(), gspeed.std())
