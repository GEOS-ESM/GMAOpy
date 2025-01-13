import sys
from semperpy.core.tools import to_list, apply_type
from semperpy.core.configure import Configure
from semperpy.core.configfile import ConfigFile

class MergeXRef(object):

    def __init__(self,application,other,reference=None):
        if reference is None:
            configure = Configure(application)
            filename = 'xref.def'
            ref = ConfigFile(configure.file(filename,'CONFIG','ods')[0])
        else:
            ref = ConfigFile(reference)
        new = ConfigFile(other)

        config = dict(
            kt = dict(
                isInt = True, addTo = True
            ),
            kx = dict(
                isInt = True, addTo = True
            ),
            levels = dict(
                isInt = False, addTo = False,isFloat = True
            ),
            files = dict(
                isInt = False, addTo = True, isFloat = False
            ),
            leveltypes = dict(
                isInt = False, addTo = False, isFloat = False
            ),
        )
        self.config_ = ref
        for var in ['kx','kt','files','levels','leveltypes']:
            for k in new[var].keys():
                if not k in ref[var]:
                    ref[var][k] = to_list(new[var][k])
                else:
                    news = set(to_list(new[var][k]))
                    refs = set(to_list(ref[var][k]))
                    if config[var]['addTo']:
                        n = list(news.union(refs))
                    elif news != refs:
                        raise ValueError('in entry %s, values are different' % k)
                    n = list(refs)
                    if config[var]['isInt']:
                        n = apply_type(int,n)
                    elif config[var]['isFloat']:
                        if var=='levels' and ref['leveltypes'][k]=='pl':
                            n = apply_type(float,n)
                        else:
                            n = apply_type(int,n)
                    n.sort()
                    if not config[var]['isInt'] and not config[var]['isFloat']:
                        n = apply_type(str,n)
                    ref[var][k] = n

    def __str__(self):
        c = self.config_
        lines = []
        for var in ['kx','kt','files','levels','leveltypes']:
            lines.append('[%s]' % var)
            result = c[var]
            keys = result.keys()
            if var == 'kt' or var == 'kx':
                keys = apply_type(int,keys)
            keys.sort()
            for  k in keys:
                lines.append('%s = %s' % (k,','.join(to_list(apply_type(str,result[str(k)])))))
            lines.append('')
        return '\n'.join(lines)
