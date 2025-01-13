from semperpy.core.tools import is_string

class FileStorer(object):

    def __init__(self,filename):
        self.file_ = open(filename,'w')
        self.header_ = None

    def __del__(self):
        self.close()

    def close(self):
        if self.file_:
            self.file_.close()
            self.file_ = None

    def __call__(self,record):
        if not self.header_:
            self.header_ = list(record.keys())
            self.writeln('|'.join(self.header_))
        values = list(record.values())
        for i in range(len(values)):
            if not is_string(values[i]):
                values[i] = str(values[i])
        self.writeln('|'.join(values))

    def writeln(self,s):
        self.file_.write(s)
        self.file_.write('\n')
