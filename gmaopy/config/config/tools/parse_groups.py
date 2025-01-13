import re
from semperpy.core.tools import apply_type

all = []
f = open('combinations.m')
lines = f.readlines()
f.close()

levels = [1000,925,850,700,500,400,300,250,200,150,100,70,50,30,20,10,7,5]

def getValues(value):
    if value is None:
        return None
    value = value.groups()[0]
    result = []
    m = re.match('\[(.*?)\]',value)
    if m:
        result = apply_type(int,m.groups()[0].split(' '))
    else:
        result.append(int(value))
    return result

def new_dict():
    return dict(
        kt = None,
        kx = None,
        title = None,
        level = None
    )

d = new_dict()
for line in lines:
    line = re.sub('\n','',line)
    if line != '':
        if line == 'k = k + 1;':
            all.append(d)
            d = new_dict()
        kt = getValues(re.match('.*?\.kt = (.*?);',line))
        if not kt is None:
            d['kt'] = kt
        kx = getValues(re.match('.*?\.kx = (.*?);',line))
        if not kx is None:
            d['kx'] = kx
        title = re.match('.*?\.id = (.*?);',line)
        if not title is None:
            d['title'] = title.groups()[0]
        level = re.match('.*?\.plev = (.*?);',line)
        if not level is None:
            level = level.groups()[0]
            if level == 'plev':
                d['level'] = levels
            else:
                m = re.match('\[(.*?)\]',level)
                if m:
                    d['level'] = apply_type(float,m.groups()[0].split(' '))
                else:   
                    m = re.match('plev.*?plev>=(.*?)\)',level)
                    if m:
                        value = float(m.groups()[0])
                        indx = levels.index(value)
                        d['level'] = levels[0:indx+1]
for d in all:
    if True or d['kt'] is not None and d['kx'] is not None:
        title = d['title']
        t = title.lower()
        # substitute space, slash and braquets with underscore
        t = re.sub('[ \/\(\)\-\,]','_',t)
        # remove possible double underscores
        t = re.sub('__','_',t)
        # remove possible underscores at the beginning and the end of the string
        t = re.sub('_$','',re.sub('^_','',t))
        print('[%s]' % t)
        print('title =',title)
        if d['kt'] is None:
            print('kt = None')
        else:
            print('kt = ',','.join(apply_type(str,d['kt'])))
        if d['kx'] is None:
            print('kx = None')
        else:
            print('kx = ',','.join(apply_type(str,d['kx'])))
        if d['level'] is None:
            print('level = None')
        else:
            print('level =',','.join(apply_type(str,d['level'])))
        print()
