from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.fields.netcdf.odasfilereader import ODASFileReader

config = GMAOConfig(ignore_missing=True,verbose=10)
r = ODASFileReader('odas.1993030403.nc',config)
a,f = r.slice(dict(
    date = 1993030403,
    level = [0,450],
    lat = [-90,-30],
    lon = [0,70],
    parameter = 'T'
))
