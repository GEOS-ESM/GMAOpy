from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.core.index import Index
from semperpy.fields.netcdf.file import File
from semperpy.plot.basemap import *
from semperpy.fields.domain import Domain

r = File('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM',GMAOConfig(ignore_missing=True,verbose=10))

domains = Domain.domains()
domain = domains['n.amer']


directive = dict(
    parameter = 'slp',
    level = 0,
    date = [2003111300,2003111309],
    #lat = domain.latitudes(),
    #lon = domain.longitudes(),
)

indx = Index(*(r.dimension_official_names() + ['level','step','type']))

t,fieldset = r.slice(directive,index=indx,step=0,type='fc')
print(indx)
