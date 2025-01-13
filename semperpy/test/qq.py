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
r = File('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM',GMAOConfig(ignore_missing=True,verbose=10))

#   XYT slices with lat/lon subsetting
#   ----------------------------------
ga('set lon 170 320') 
ga('set lat -20 50')  
ga('set time 0Z5feb2003 21Z5feb2003') # 1 day worth of data
gslp = ga.expr('slp')/100.0-1000.0

directive = dict(
    parameter = 'slp',
    date = [2003020500,2003020521],
    longitude = [170,-40],
    latitude = [-20,50]
)
slp,fieldset = r.slice(directive)
slp = slp / 100.0 - 1000.0
print(slp.shape,gslp.shape)
print(slp.mean(), gslp.mean())
print(slp.std(), gslp.std())
