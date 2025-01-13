from semperpy.language.validate import validateChoice
from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.fields.netcdf.file import File
from pylab import *
from pylab import prctile

#   Start GrADS and open the data file
#   ----------------------------------
r = File('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM',GMAOConfig(ignore_missing=True,verbose=10))

print("speed")
directive = dict(
    parameter = 'u',
    level = [300,200],
    date = [2003111312,2003111321],
    lon = [-140,-40],
    lat = [20,50]
)

u = r[directive]
directive['parameter'] = 'v'
v = r[directive]
speed = u * u + v * v
speed = sqrt(speed)

v = 2003111312
i = 0
l = [300,250,200]
while v <= 2003111321:
    print(v)
    for j in 0,1,2:
        print(i,j)
        speed[i][j] = v*1000.0 + l[j]
    v+=3
    i+=1
print(speed)
