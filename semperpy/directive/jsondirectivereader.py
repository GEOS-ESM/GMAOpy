import os
from glob import glob
from semperpy.core.configure import Configure
from semperpy.directive.jsonfile import JSonFile

class JSonDirectiveReader(object):
    
    def __init__(self,prefix):
        configure = Configure(prefix)
        self.path_ = configure.path('LANGUAGE',walk=True)

    def __call__(self,name):
        for path in self.path_:
            filename = JSonFile.path(path,name)
            if os.path.exists(filename):
                return JSonFile(path)(name)
        raise SystemError('Could not find a file for %s in %s' % (name,','.join(self.path_)))

    def directiveList(self):
        all = []
        for path in self.path_:
            file_list = glob(path + '/*.json') 
            for file in file_list:
                try:
                    dir = JSonFile()(file)
                    if 'doc' in dir:
                        all.append(dir['directive'])
                except:
                    print(file)
                    raise
        return all
