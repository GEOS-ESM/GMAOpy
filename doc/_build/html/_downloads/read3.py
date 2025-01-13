import os
from semperpy.netcdf.file import File
import gmaopy.netcdf # register dimensions specific to our files

datapath = os.getenv('SEMPERPY_TESTDATA')
reader = File(datapath + '/an.hdf')
directive = dict(
    variable = 't',
    date = 2010071000,
    latitude = {20:90},
    longitude = {120:250},
    level = [1000,500]
)
w = reader.readArray(directive)
print("shape: %s, mean: %f" % (w.shape, w.mean()))
