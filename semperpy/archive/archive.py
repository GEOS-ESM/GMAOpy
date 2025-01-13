import os
from semperpy.core.decorators import abstractMethod

class Archive(object):

    archives_ = {}

    def __init__(self,filelist):
        filelist = [ x for x in list(set(filelist)) if os.path.exists(x) ]
        if len(filelist) > 0:
            self.stagelist_ = self.offline(filelist)
        else:
            self.stagelist_ = filelist

    def stage(self):
        if len(self.stagelist_) > 0:
            print('staging files:\n%s' % '\n'.join(self.stagelist_))
            self.do_stage(self.stagelist_)
        else:
            print('no staging necessary')

    def copy(self,destination):
        self.do_copy(self.stagelist_,destination)

    def stageCount(self):
        return len(self.stagelist_)

    def stageSize(self):
        size = 0.0
        for x in self.filesize(self.stagelist_):
            size += x
        return size / 1024.0 / 1024.0

    @abstractMethod
    def do_stage(self,stagelist):
        pass

    @abstractMethod
    def offline(self,filelist):
        pass

    @abstractMethod
    def filesize(self,filelist):
        pass

    @abstractMethod
    def do_copy(self,filelist,destination):
        pass

    @classmethod
    def register(self,name,klass):
        self.archives_[name] = klass

    @classmethod
    def create(self,name,*args,**kargs):
        if not name in self.archives_:
            raise SystemError('Archive %s in unknown' % name)
        return self.archives_[name](*args,**kargs)
