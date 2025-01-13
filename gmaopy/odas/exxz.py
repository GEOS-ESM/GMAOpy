from extract_xz_slice import *

from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.fields.netcdf.odasfilereader import ODASFileReader

config = GMAOConfig(ignore_missing=True,verbose=10,use_intervals=True)
r = ODASFileReader('odas.1993030403.nc',config)
a,f = r.slice(dict(
    date = 1993030403,
    level = [0,500],
    latitude = [0.13],
    #lon = [135,-95], #eqpac
    #lon = [44,96], #eqind
    #lon = [-44,6], #eqatl
    longitude = [],
    parameter = 'T'
))
print(a.shape)
print(a.mean())

b = ext('odas.1993030403.nc','fcst','T',[0,500],'glb',0.124951)
print(b.data.shape)
print(b.data.mean())
