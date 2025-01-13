import re
from glob import glob
import numpy as np
from semperpy.core.tools import apply_type,dictionary,to_list
from semperpy.core.configure import Configure
from semperpy.core.configfile import ConfigFile
from gmaopy.ods.ods import ODS

class XReference(object):

    def __init__(self,files,names):
        self.files_ = files
        self.names_ = names
        self.levels_ = self.readLevels()

    def readLevels(self):
        c = Configure('semperpy')
        config = ConfigFile(c.file('levels.def','CONFIG','ods'))
        if len(config) == 0:
            config['levels'] = {}
            config['leveltypes'] = {}
        return config

    def build(self):
        files = dictionary()
        kx = dictionary()
        kt = dictionary()
        levels = dictionary()
        for i,file in enumerate(self.files_):
            file_list = glob(file)
            for f in file_list:
                name = self.names_[i]
                l = ''
                if name != '':
                    l = f
                    l = l.split('/')
                    l = l[-1]
                    l = re.findall(name,l)
                    if len(l) > 0:
                        l = l[0]
                ff = ODS(f)
                self.build_one(ff,kt,kx,levels,files,l)
        levtypes = {}
        keys = levels.keys()
        delete = []
        for k in keys:
            if k in self.levels_['levels']:
                leveltype = self.levels_['leveltypes'][k]
                levels[k] = set(to_list(self.levels_['levels'][k]))
            else:
                z = list(levels[k])
                y = [ int(x) for x in z ]
                if set(y).issubset(set(ODS.stdlevels_)):
                    leveltype = 'pl'
                elif len(y) == 1:
                    if y[0] == 0:
                        leveltype = 'sfc'
                    else:
                        leveltype = 'unknown'
                    delete.append(k)
                elif z == y:
                    y.sort()
                    result = np.zeros(len(y)-1)
                    for i in range(1,len(y)):
                        result[i-1] = y[i] - y[i-1]
                    if result.mean() == 1:
                        leveltype = 'ch'
                    else:
                        leveltype = 'unknown'
                        delete.append(k)
                else:
                    leveltype = 'unknown'
                    delete.append(k)
            levtypes[k] = leveltype
        for k in delete:
            del(levels[k])
        levels['00000-00000'] = set(ODS.stdlevels_)
        levtypes['00000-00000'] = 'pl'
        self.config_ = dict(
            kt = kt,
            kx = kx,
            levels = levels,
            files = files,
            leveltypes = levtypes,
        )

    def __str__(self):
        lines = []
        c = self.config_
        for var in ['kx','kt','files','levels','leveltypes']:
            lines.append('[%s]' % var)
            keys = list(c[var].keys())
            keys.sort()
            for k in keys:
                if type(c[var][k]) == set:
                    i = list(c[var][k])
                else:
                    i = [c[var][k]]
                if var == 'levels':
                    if c['leveltypes'][k] == 'ch':
                        i = apply_type(int,i)
                        i.sort()
                    elif c['leveltypes'][k] == 'pl':
                        i = apply_type(float,i)
                        i.sort()
                    elif c['leveltypes'][k] == 'depth':
                        i = apply_type(float,i)
                        i = apply_type(int,i)
                        i.sort()
                    elif c['leveltypes'][k] == 'sfc':
                        i = 0
                    elif c['leveltypes'][k] == 'wl':
                        i = apply_type(float,i)
                        i = apply_type(int,i)
                        i.sort()
                    else:
                        raise RuntimeError('need to add code for level type "%s"' % c['leveltypes'][k])
                else:
                    i.sort()
                i = apply_type(str,i)
                lines.append('%s = %s' % (k,','.join(i)))
            lines.append('')
        return '\n'.join(lines)



    def build_one(self,f,kt_sets,kx_sets,levels,files,file):
        batchlen = len(f.file_.dimensions['batchlen'])
        date = list(f.synops_.keys())[0]
        count = f.synops_[date]['length'] // batchlen
        remaining = f.synops_[date]['length'] % batchlen
        kts = f.extract('kt').values()
        kts = kts.flatten()
        actual = count * batchlen + remaining
        kts = kts[0:actual]
        kts = list(set(kts))
        for kt in kts:
            filter = f.compile('kt == %d' % int(kt),False)
            kxs = set(f.extract('kx',filter).values())
            levs = set(f.extract('lev',filter).values())
            if not kt in kt_sets:
                kt_sets[kt] = set()
            kt_sets[kt] = kt_sets[kt].union(kxs)
            for kx in list(kxs):
                if not kx in kx_sets:
                    kx_sets[kx] = set()
                kx_sets[kx].add(kt)
                hash = '%05d-%05d' % (int(kx),int(kt))
                if not hash in levels:
                    levels[hash] = set()
                levels[hash] = levels[hash].union(levs)
                if not hash in files:
                    files[hash] = set()
                if file != '':
                   files[hash].add(file)
