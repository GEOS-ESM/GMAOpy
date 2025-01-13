from semperpy.language.validate import validateChoice
from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.fields.netcdf.file import File
from pylab import *

r = File('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM',GMAOConfig(ignore_missing=True,verbose=0))

directive = dict(
    parameter = 'SLP',
    date = [2003020500,2003020521],
)
slp,fieldset = r.slice(directive)
slp = slp / 100.0 - 1000.0
print(slp.shape)
print(slp.mean())
print(slp.std())

directive = dict(
    parameter = 'slp',
    date = [2003020500,2003020521],
    lon = [-140,-40],
    lat = [20,50]
)
slp,fieldset = r.slice(directive)
slp = slp / 100.0 - 1000.0
print(slp.shape)
print(slp.mean())
print(slp.std())

directive = dict(
    parameter = 'u',
    level = [300,200],
    date = [2003111312],
    lon = [-140,-40],
    lat = [20,50]
)

u,fieldset = r.slice(directive)
directive['parameter'] = 'v'
v,fieldset = r.slice(directive)
speed = sqrt((u * u) + (v * v))
print(speed.shape)
print(speed.mean())
print(speed.std())
