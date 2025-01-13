import os
from semperpy.netcdf.file import File
import gmaopy.netcdf # register dimensions specific to our files

datapath = os.getenv('SEMPERPY_TESTDATA')
reader = File(datapath + '/an.hdf')
directive = dict(
    variable = 't',
    date = 2010071000,
    level = {1000:500},
    latitude = [0,10,20,30,40,50]
)
w = reader.readBundle(directive)
print()
print(len(w))
print()
for field in w:
    print(field.shape())
    print("level %s" % field.get('level'))
    print("latitude %f" % field.get('latitude'))
    print()
