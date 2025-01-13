import os
import sys
from netCDF4 import Dataset

if len(sys.argv) < 2:
    raise SystemError('usage: path')
path = sys.argv[1]
files = os.listdir(path)
expvers = set()
dimensions = set()
variables = {}
collections = {}

for file in files:
    components = file.split('.') 
    if len(components) != 4:
        raise ValueError('The file name %s cannot be analysed, it is not in a known format' % file)
    expver,collection,dates,extension = components
    expvers.add(expver)
    if not collection in collections:
        collections[collection] = set()
    f = Dataset(path + '/' + file)
    for d in f.dimensions:
        dimensions.add(f)
    for v in [ x for x in list(f.variables.keys()) if not x in f.dimensions ]:
        v = v.lower()
        if not v in variables:
            variables[v] = set()
        variables[v].add(collection)
        collections[collection].add(v)

print('[variables]')
vars = list(variables.keys())
vars.sort()
print('list = %s' % ','.join(vars))
for k in vars:
    l = list(variables[k])
    l.sort()
    print(k,'=',','.join(l))
print()
print('[collections]')
colls = list(collections.keys())
colls.sort()
print('list = %s' % ','.join(colls))
for k in colls:
    l = list(collections[k])
    l.sort()
    print(k,'=',','.join(l))
