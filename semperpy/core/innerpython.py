import imp
import sys
import inspect

#----------------------------------------------------------------------------
# SemperPy Copyright SynopticView 2009-2010
#
# Claude Gibert, December 2009, dev@synopticview.com
#-------------------------------------------------------------------
# Trying to keep python introspection centralized in one single
# place to be able to face big changes.
# This code was partially copied from the Python CookBook and
# some recipes on ActiveState.
#
# Once requested and found, classes and modules are cached to 
# speed up the next request.
#-------------------------------------------------------------------
class InnerPython(object):

    classes     = {}
    modulecache = {}

    @classmethod
    def get_class(self,name):
        if name in self.classes:
            return self.classes[name]
        c = self._get_class(name)
        self.classes[name] = c
        return c

    @classmethod
    def _get_class(self,name):
        l = name.split('.')
        modulename = None
        if len(l) > 0:
            classname = l.pop()
            modulename = '.'.join(l)
        else:
            classname = l[0]
        if modulename:
            object = self.in_globals(classname)
            if object and object.__module__ == modulename:
                return object
            module = self.load_module(modulename)
            return module.__dict__[classname]
        object = self.in_globals(classname)
        if object:
            return object
        object = self.in_globals('__builtins__')
        return object[classname]

    @classmethod
    def in_globals(self,name):
        o = inspect.getouterframes(inspect.currentframe())
        current = o[0][1]
        while o[0][1] == current:
            o.pop(0)
        for frame in o:
            if name in frame[0].f_globals:
                return frame[0].f_globals[name]

    @classmethod
    def load_module(self,name):
        if name in sys.modules:
            return sys.modules[name]
        object = self.in_globals(name)
        if object and inspect.ismodule(object):
            return object
        if not name in self.modulecache:
            self.modulecache[name] = self._find_module(name)
        return self.modulecache[name]

    @classmethod
    def _find_module(self,name):
        l = name.split('.')
        path = None
        object = None
        while len(l) > 0:
            n = l.pop(0)
            file, fname, desc = imp.find_module(n,path)
            try:
                object = imp.load_module(n, file, fname, desc)
            finally:
                if file != None:
                    file.close()
            if '__path__' in object.__dict__:
                path = object.__path__
        return object        

