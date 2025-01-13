import os
from semperpy.netcdf.file import File
import gmaopy.netcdf # register dimensions specific to our files

datapath = os.getenv('SEMPERPY_TESTDATA')
reader = File(datapath + '/an.hdf')
directive = dict(
    variable = 't',
    date = 2010071000,
    level = {1000:500}
)
w = reader.readBundle(directive)
print()
print(len(w))
print()
for field in w:
    print(field.shape())
    print(field.get('level'))
    print(field.get('date'))
    print()
