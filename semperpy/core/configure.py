#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2010
#
# Claude Gibert, June 2010, dev@synopticview.com
#-------------------------------------------------------------------
from semperpy.core.tools import dirlist
import os

class Configure(object):

    def __init__(self,prefix):
        self.prefix_ = prefix
        
    def localise(self):
        v = os.getenv('SP_LOCATION')
        if v is None:
            return ''
        else:
            return '_' + v

    def path(self,name,subpath='',walk=False):
        var = name.lower()
        result = []
        paths = [ x for x in os.getenv(self.variableName(name),'./').split(':') if x != '']
        for p in paths:
            p = self.resolvePath(p)
            if len(subpath) > 0:
                if p[-1] != '/':
                    p += '/'
                p += subpath
            if walk:
                result += dirlist(p)
            else:
                result.append(p)
        return result

    def file(self,filename,name,subpath=''):
        where = self.path(name,subpath)
        result = []
        for p in where:
            fullpath = p + '/' + filename
            if os.path.exists(fullpath):
                result.append(fullpath)
        return result

    def resolvePath(self,path):
        if (path[0] != '/' and path[0] != '.') or path[0] == '~':
            if path[0] == '~':
                path = path[1:]
                if path[0] == '/':
                    path = path[1:]
            return os.getenv(self.variableName('config'),'.') + '/' + path
        else:
            return path

    def variableName(self,variable):
        name = variable
        if self.prefix_ != '':
            name = self.prefix_ + '_' + variable
        return name.upper()
