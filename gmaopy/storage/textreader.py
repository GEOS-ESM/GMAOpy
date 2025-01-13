import re
from semperpy.core.tools import to_list
from semperpy.core.decorators import abstractMethod
from semperpy.core.index import Index
from semperpy.geo.domain import Domain
from gmaopy.storage.reader import Reader

class TextReader(object):

    header_ = None
    floats_ = None

    def __init__(self,files,generic=None,check_domains=True,dry_run=False,missing_value=None):
        if missing_value is not None:
            missing_value = float(missing_value)
        files = to_list(files)
        if self.header_ is None:
            if generic is not None:
                header = list(generic.keys())
                header.sort()
            else:
                header = self.readHeader(files[0])
            TextReader.header_ = header
            floats = {}
            for h in header:
                floats[h] = True
            for i,k in enumerate(header):
                try:
                    f = float(generic[k])
                except:
                    floats[k] = False
            TextReader.floats_ = floats
        self.header(self.header_)
        domains = Domain.domains('semperpy')
        for filename in files:
            f = open(filename,'r')
            f.seek(0,2)
            length = f.tell()
            f.seek(0,0)
            count = 0
            h = f.readline()[0:-1]
            count += len(h)
            h = h.split('|')
            if set(h) != set(self.header_):
                raise ValueError('in file %s the header is different from the prototype' %filename)
            self.header_ = h
            line = f.readline()
            while line != '':
                line = line[0:-1]
                count += len(line)
                values = line.split('|')
                directive = {}
                for j,key in enumerate(self.header_):
                    v = values[j]
                    if self.floats_[key]:
                        v = float(v)
                    directive[key] = v
                if check_domains and directive['domain_name'] in domains:
                    theirs = Domain(directive['north'],directive['west'],directive['south'],directive['east'])
                    if not theirs == domains[directive['domain_name']]:
                        raise ValueError('A domain has a different geographical definition from the configuration file, please check the coordinates or rename that domain. Yours: %s, %s: %s' % (str(theirs),directive['domain_name'],str(domains[directive['domain_name']])))
                if not dry_run:
                    self.directive(directive,count,length)
                line = f.readline()
            f.close()

    def readHeader(self,file):
        f = open(file,'r')
        line = f.readline()
        f.close()
        h = line[0:-1].split('|')
        h.sort()
        return h

    @abstractMethod
    def header(self,header):
        pass

    @abstractMethod
    def directive(self,directive,count,totalcount):
        pass
