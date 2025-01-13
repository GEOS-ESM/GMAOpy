from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.fields.netcdf.file import File
from semperpy.plot.basemap import *
from semperpy.fields.domain import Domain

r = File('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM',GMAOConfig(ignore_missing=True,verbose=10))

domains = Domain.domains()
domain = domains['n.amer']

directive = dict(
    parameter = 't',
    level = [300],
    date = [2003111300,2003111309],
    #lat = domain.latitudes(),
    #lon = domain.longitudes(),
)

geography = Geography(
                  projection='stereo',
                  hemisphere='south',
                  lon_0=270,
)
p = FieldPlotter(layout=[2,2])
a,fieldset = r.slice(directive)
for f in fieldset:
    print(f.get('date'))
    p(f,geography,ContourFill())
p.draw('/Users/claudegibert/Desktop/test')
