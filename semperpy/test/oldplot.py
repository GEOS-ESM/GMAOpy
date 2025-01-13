from pylab import gcf
from semperpy.language.validate import validateChoice
from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.fields.netcdf.file import File
from semperpy.plotting.basemap.plot import Plot

r = File('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM',GMAOConfig(ignore_missing=True))

directive = dict(
    parameter = 't',
    level = [300],
    date = [2003111312,2003111318],
    lat = [-20,80],
    lon = [-140,30],
)

t,indx = r[directive]
d = indx.access(date=20031113120000)[0]
p = Plot(d.grid())
p.contourf(d)
d = indx.access(date=20031113180000)[0]
p.contourf(d)

print('done')
