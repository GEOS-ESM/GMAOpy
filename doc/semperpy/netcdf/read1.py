import os
from semperpy.netcdf.file import File
import gmaopy.netcdf # register dimensions specific to our files

datapath = os.getenv('SEMPERPY_TESTDATA')
reader = File(datapath + '/an.hdf')
directive = dict(
    variable = 't',
    date = 2010071000,
    level = 500
)
w = reader.readArray(directive)
print()
print("shape: %s, mean: %f" % (w.shape, w.mean()))
