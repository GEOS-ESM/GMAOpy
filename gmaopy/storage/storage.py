from semperpy.core.tools import mergedicts_overwrite

class Storage(object):

    @classmethod
    def register(self,name,what):
        self.factory_.register(name,what)

    @classmethod
    def create(self,expr,*args,**kargs):
        s = expr.split(':')
        storer = s[0].strip()
        params = ''
        if len(s) > 1:
            params = s[1]
            params = params.split(',')
            a = {}
            for p in params:
                name,value = p.split('=')
                name = name.strip()
                value = value.strip()
                a[name] = value
            kargs = mergedicts_overwrite(kargs,a)
        return self.factory_.create(storer,*args,**kargs)
