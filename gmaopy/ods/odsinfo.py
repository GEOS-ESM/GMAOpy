from collections import defaultdict
from semperpy.core.tools import to_list, apply_type, dictionary
from semperpy.core.configure import Configure
from semperpy.core.configfile import ConfigFile

class ODSInfo(object):

    cache_ = {}
    def __init__(self):
        configure = Configure('semperpy')
        filename = 'xref.def'
        if not filename in self.cache_:
            config = ConfigFile(configure.file(filename,'CONFIG','ods'))
            # we load the file and create a copy in memory. We need to convert
            # kx and kt values to int, and organise the data in a way which is
            # useful. Ugly code.
            conf = {}
            # convert right hand side of sections kx and kt to sets of ints
            for section in ['kx','kt']:
                d = dictionary()
                for k,i in config[section].items():
                    d[int(k)] = set(to_list(apply_type(int,i)))
                conf[section] = d
            # convert left hand side of sections kx_files and kt_files to ints
            d = dictionary()
            for k,i in config['files'].items():
                l = k.split('-')
                kx = int(l[0])
                kt = int(l[1])
                if not kx in d:
                    d[kx] = {}
                d[kx][kt] = to_list(i)
            conf['files'] = d
            # copy the section 'file' and all file entries, converting the right
            # hand side to lists of ints
            conf['lev_kx'] = dictionary()
            for k,i in config['leveltypes'].items():
                kx,kt = apply_type(int,k.split('-'))
                if not kx in conf['lev_kx']:
                    conf['lev_kx'][kx] = dictionary()
                    if not kt in conf['lev_kx'][kx]:
                        conf['lev_kx'][kx] = dictionary()
                conf['lev_kx'][kx][kt] = i
            conf['predef_kx'] = defaultdict(dict)
            for k,i in config['levels'].items():
                kx,kt = apply_type(int,k.split('-'))
                if conf['lev_kx'][kx][kt] == 'ch':
                    conf['predef_kx'][kx][kt] = tuple(apply_type(int,i))
                else:
                    conf['predef_kx'][kx][kt] = tuple(apply_type(float,to_list(i)))
            self.cache_[filename] = conf
        self.config_ = self.cache_[filename]

    def fileNameOf(self,kx,kt):
        return self.config_['files'][kx][kt]

    def levelsOf(self,kx,kt):
        leveltype = 'sfc'
        leveltype = self.config_['lev_kx'][kx][kt]
        if leveltype == 'sfc':
            levels = (0,)
        elif kx in self.config_['predef_kx'] and kt in self.config_['predef_kx'][kx]:
            levels = self.config_['predef_kx'][kx][kt]
        elif leveltype == 'pl':
            levels = self.config_['predef_kx'][0][0]
        else:
            raise ValueError('"%s" is an unknown type of level' % leveltype)
        return leveltype,levels

    def kxs(self):
        return self.config_['kx'].keys()

    def kts(self):
        return self.config_['kt'].keys()

    def kx(self,kt):
        if not kt in self.config_['kx']:
            return set()
        return self.config_['kx'][kt]

    def kt(self,kx):
        if not kx in self.config_['kt']:
            return set()
        return self.config_['kt'][kx]

    def knows(self,kx,kt):
        return (kx in self.config_['kx']) and (kt in self.config_['kx'][kx])

    def show(self):
        kx = self.config_['kx']
        kt = self.config_['kt']
        kt_files = self.config_['kt_files']
        kx_files = self.config_['kx_files']
        levtypes = self.config_['levtypes']
        print('[kx]')
        index = kx.keys()
        index.sort()
        for k in index:
            i = kx[k]
            print(k,'=',','.join(apply_type(str,list(i))))
        print()
        print('[kt]')
        index = kt.keys()
        index.sort()
        for k in index:
            i = kt[k]
            print(k,'=',','.join(apply_type(str,list(i))))
        print()

        print('[kx_files]')
        index = kx_files.keys()
        index.sort()
        for k in index:
            print(k,'=',','.join(list(kx_files[k])))
        print()
        print('[kt_files]')
        index = kt_files.keys()
        index.sort()
        for k in index:
            print(k,'=',','.join(list(kt_files[k])))
        print()
        codes = {}
        for k in self.config_['predef_kx'].keys():
            for l in self.config_['predef_kx'][k].keys():
                codes['%03d-%03d' % (k,l)] = self.config_['predef_kx'][k][l]
        keys = codes.keys()
        keys.sort()
        print('[levels]')
        for k in keys:
            print('%s = %s' % (k,','.join(apply_type(str,codes[k]))))
        print()
        print('[leveltypes]')
        keys = levtypes.keys()
        keys.sort()
        for k in keys:
            print('%s = %s' % (k,levtypes[k]))
