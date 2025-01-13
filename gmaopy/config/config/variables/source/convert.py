import re

f = open('u')
lines = f.readlines()
i = 0
all = {}
for line in lines:
    i += 1
    line  = re.sub('\n','',line)
    cols = line.split('|')
    if len(cols) != 3:
        raise ValueError('line %d: not 3 columns' % i)
    param,title,unit = [ x.strip() for x in cols ]
    param = param.lower()
    if not param in all:
        all[param] = dict(
            title = title,
            unit = unit,
            line = i
        )
    else:
        t = all[param]['title']
        u = all[param]['unit']
        l = all[param]['line']
        if t != title or u != unit:
            raise ValueError('\nmismatch: line %d, %s, %s\n          line %d, %s, %s' % (l,t,u,i,title,unit))

params = list(all.keys())
params.sort()
print("[titles]")
for param in params:
    print(param,'=',all[param]['title'])
print()
print("[units]")
for param in params:
    print(param,'=',all[param]['unit'])
