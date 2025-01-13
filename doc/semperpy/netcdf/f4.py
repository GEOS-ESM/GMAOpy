from semperpy.core.date import Dates
from semperpy.netcdf.file import File
import gmaopy.netcdf # register dimensions specific to our files

reader = File('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM')
directive = dict(
    variable = 'u',
    date = Dates(2001010100,2001013118,6),
    level = 850,
)
w = reader.readBundle(directive)
print()
print(len(w))

