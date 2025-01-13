import sys
from gmaopy.modules.obsload import *

if len(sys.argv) != 3:
    raise ValueError('arguments...')

which=sys.argv[1]
database=sys.argv[2]

textloader(
    files = which,
    database = database,
    overwrite = False
)
