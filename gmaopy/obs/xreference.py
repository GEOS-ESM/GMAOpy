import copy
import re
from semperpy.directive.directive import Directive
from gmaopy.retrieve.retriever import Retriever
from gmaopy.ods.xreference import XReference as XRef

class XReference(Directive):

    def __init__(self,*args,**kargs):
        super(XReference,self).__init__(*args,**kargs)
        self.checkLanguage()
        paths = []
        files = []
        dir = copy.copy(self)
        for date in self['date']:
            dir['date'] = date
            path = Retriever.full_path(dir,'semperpy') + '/' + self['mask']
            paths.append(path)
            file_name = Retriever.datedFile(dir,'semperpy')
            filename = re.sub('<collection>','(.*?)',file_name)
            if filename == file_name:
                filename = ''
            else:
                filename = re.sub('\+','\+',filename)
                filename = re.sub('\-','\-',filename)
                l = filename.split('/')
                filename = l[-1]
            files.append(filename)
        xref = XRef(paths,files)
        xref.build()
        print(xref)

xreference = XReference
