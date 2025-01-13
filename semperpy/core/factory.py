#----------------------------------------------------------------------------
# SemperPy Copyright SynopticView, GMAO 2009-2010
#
# Claude Gibert, December 2009, dev@synopticview.com
#----------------------------------------------------------------------------
# Just a wrapper for a dictionay of functions and classes.
# different behaviour can be specified:
# - raise an exception if the same name is registered twice or not (entry 
#   is overriden).
# - when creating / calling, if the name is unknown, looks for a special
#   name "default" which is executed by default or not (fails).
# The default is "fail if an name is registered twice", "try to execute
# default if present".
#----------------------------------------------------------------------------

class Factory(dict):

    def __init__(self,noduplicates = True,hasdefault = True):
        self.noduplicates = noduplicates
        self.hasdefault = True
        super(Factory,self).__init__()

    def register(self,name,what):
        if name in self and self.noduplicates:
            raise IndexError('Factory already has an entry: "' + what.__str__() + '"')
        self[name] = what

    def create(self,what,*args,**kargs):
        if not what in self:
            if self.hasdefault and '__default__' in self:
                return self['__default__'](*args,**kargs)
            else:    
                raise IndexError('Factory does not know how to create "%s", known entries: %s ' % (what.__str__(),'\n'.join([ str(x) for x in list(self.keys()) ])))
        return self[what](*args,**kargs)

    def get(self,what):
        if not what in self:
            if self.hasdefault and '__default__' in self:
                return self['__default__']
            else:    
                raise IndexError('Factory does not know how to create "' + what.__str__() + '"')
        return self[what]

class SingletonFactory(Factory):

    def __init__(self,*args,**kargs):
        super(SingletonFactory,self).__init__(*args,**kargs)
        self.cache = {}

    def create(self,what,*args,**kargs):
        if not what in self.cache:
            o = super(SingletonFactory,self).create(what,*args,**kargs)
            self.cache[what] = o
        return self.cache[what]
