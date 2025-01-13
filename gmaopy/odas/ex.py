from extract_yz_slice import *
from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.fields.netcdf.odasfilereader import ODASFileReader

config = GMAOConfig(ignore_missing=True,verbose=10)
r = ODASFileReader('odas.1993030403.nc',config)
a,f = r.slice(dict(
    date = 1993030403,
    level = [0,500],
    lat = [-30,30],
    lon = [-155],
    parameter = 'T'
))
print(a.shape)
print(a.mean())

b = ext('odas.1993030403.nc','fcst','T',[0,500],'p155W')
print(b.data.shape)
print(b.data.mean())
