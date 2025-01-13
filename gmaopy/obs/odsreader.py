import copy
from gmaopy.retrieve.retriever import Retriever
from semperpy.geo.domain import Domain
from gmaopy.ods.ods import ODS
from gmaopy.ods.odsgroup import ODSGroup
from gmaopy.storage.reader import Reader
from gmaopy.obs.obsexpander import ObsExpander

class ODSReader(object):

    def __init__(self,*args,**kargs):
        pass

    def __call__(self,directive,columns,**kargs):
        unique = set()
        all = ObsExpander.expand_for_storage(directive,unique)
        retriever = Retriever('semperpy','hourly',all)
        var = {}
        for date,files in retriever.files():
            for file in files:
                ods = self.openODS(file)
                filter = None
                for one in files[file]['directive']:
                    if 'domain_name' in one:
                        domaindef = Domain.domains('semperpy')
                        domain = one['domain_name']
                        d = domaindef[domain]
                        if domain != 'global':
                            d = domaindef[domain]
                            expr = '(lat >= %f) & (lat <= %f) & (lon >= %f) & (lon <= %f)' % (d.south_,d.north_,d.west_,d.east_)
                            f = ods.compile(expr,False)
                            if filter is None:
                                filter = f
                            else:
                                filter |= f
                    if 'level' in one: 
                        level = one['level']
                        levelFilter = None
                        if one['levtype'] == 'pl':
                            levelFilter = ods.sampleLevels(one['level'])
                            levelFilter = levelFilter == one['level']
                        elif one['levtype'] == 'ch':
                            levelFilter = ods.read('lev')
                            levelFilter = levelFilter == one['level']
                        if levelFilter is not None:
                            if filter is not None:
                                filter &= levelFilter
                            else:
                                filter = levelFilter
                    f = ods.compile('(kx == %d) & (kt == %d)' % (one['kx'],one['kt']))
                    filter &= f
                    var[date] = ods.read(one['variable'],filter).values()
        return var
        
    def openODS(self,files):
        print(files)
        ods = None
        try:
            if len(files) > 1:
                ods = ODSGroup(files)
            else:
                ods = ODS(files[0])
        except RuntimeError or IOError as e:
            if self['ignore_missing_files']:
                print("file not found",e.message)
                print(files[0])
            else:
                raise
        return ods
    
#Reader.register('odsreader',ODSReader)
