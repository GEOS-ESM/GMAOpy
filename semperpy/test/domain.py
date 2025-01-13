from semperpy.language.validate import validateChoice
from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.fields.netcdf.file import File
from semperpy.fields.domain import Domain
from semperpy.plot.basemap import *

r = File('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM',GMAOConfig(ignore_missing=True,verbose=10))

directive = dict(
    parameter = 'SLP',
    date = [2003020500,2003020521],
)
slp,fieldset = r.slice(directive)
slp = slp / 100.0 - 1000.0
print(slp.shape)
print(len(slp))

domains = Domain.domains()
domain = domains['n.pac']
domain = domains['europe']

f = fieldset[0]
print(fieldset)
print(type(f))
print(len(f))
print(f.values_.shape)
area= f.subField(domain)
grid = area.grid()
print(len(grid.latitudes()))
print(grid.latitudes())
print(len(grid.longitudes()))
print(grid.longitudes())
print(area.shape)
print(area.size)


directive = dict(
    parameter = 'SLP',
    date = [2003020500,2003020521],
    lat = domain.latitudes(),
    lon = domain.longitudes(),
)
slp,fieldset = r.slice(directive)
print("check",fieldset[0].mean(),list(area.values()).mean())
print(area.shape)
geography = Geography(
                  projection='cyl',
)
contour = ContourFill(
                  colorbar=ColorBar(aspect=15)
)
p = FieldPlotter()
p(area,geography,contour)
p.draw()
