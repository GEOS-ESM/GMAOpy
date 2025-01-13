import sys
from semperpy.core.configfile import ConfigFile
from semperpy.core.tools import apply_type

f = ConfigFile(sys.argv[1])
levels = f['levels']
levtypes = f['leveltypes']
keys = list(levels.keys())
keys.sort()
print('[levels]')
for key in keys:
    ll = levels[key]
    if levtypes[key] == 'pl':
        ll = apply_type(float,ll)
    else:
        ll = apply_type(int,ll)
    ll.sort()
    ll = apply_type(str,ll)
    print('%s = %s' % (key,','.join(ll)))
    
