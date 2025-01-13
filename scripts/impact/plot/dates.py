import sys
from semperpy.core.configfile import ConfigFile

latest = sys.argv[1]

dates = ConfigFile('dates.def')
all = [ dates[x] for x in dates ]
all.sort(lambda a,b: cmp(a['start'],b['start']))
all[-1]['end'] = latest
for i,v in enumerate(all):
    print('[%d]' % (i+1))
    for k,i in list(v.items()):
        print('%s = %s' % (k,i))
    print()
