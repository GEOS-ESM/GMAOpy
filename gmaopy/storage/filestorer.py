import os
from semperpy.core.tools import to_list
from gmaopy.storage.storer import Storer

class FileStorer(object):

    def __init__(self,database,append = False, overwrite = False,debug = False,**kargs):
        self.file_ = None
        if not overwrite and os.path.exists(database):
            raise IOError('File %s already exists' % database)
        if append:
            self.file_ = open(database,'a')
        else:
            self.file_ = open(database,'w')
        self.header_ = None
        self.debug_ = debug

    def __del__(self):
        if self.file_ is not None:
            self.file_.close()

    def __call__(self,directives):
        directives = to_list(directives)
        for directive in directives:
            if self.header_ is None or self.debug_:
                header = list(directive.keys())
                header.sort()
                if self.debug_:
                    if not header == self.header_:
                        raise SystemError('FileStore debug: this directive is different from the previous one(s) %s' % directive)
            if self.header_ is None:
                self.header_ = header
                self.file_.write('|'.join(self.header_) + '\n')
        values = [ str(directive[x]) for x in self.header_ ]
        self.file_.write('|'.join(values) + '\n')

    def flush(self):
        self.file_.flush()

Storer.register('filestorer',FileStorer)
