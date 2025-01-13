import copy
import numpy.ma as ma
from semperpy.core.tools import to_list, is_list, nestedLoops
from semperpy.geo.domain import Domain
from semperpy.directive.directive import Directive
from gmaopy.retrieve.retriever import Retriever
from gmaopy.netcdf import *
from gmaopy.db.prrecord import PRRecord
from gmaopy.product.prodstatistics import ProdStatistics
from gmaopy.storage.storer import StorerCollection

class ProdStat(Directive):

    category_ = 'product'

    def __init__(self,*args,**kwargs):
        super(ProdStat,self).__init__(*args,**kwargs)
        self.checkLanguage()
        self.storers_ = StorerCollection(self['storage'],write = True,**self)
        all = self.distribute()
        retriever = Retriever('semperpy',self['staging_rate'],all)
        self.processData(retriever)

    def distribute(self):
        combinable = self.combinable()
        self.keepTrackOfDefaults(False)
        result = nestedLoops(self['field'][0],combinable)
        self.keepTrackOfDefaults(True)
        return result

    def combinable(self):
        return self['_combinable']

    def processData(self,retriever):
        domaindef = Domain.domains('semperpy')
        record = PRRecord()
        #----------- loop over each run -----------------------
        for date, files in retriever.files():
            #----------- loop over each file -----------------------
            for file in files:
                for field in files[file]['directive']:
                    print(file)
                    f = File(file[0])
                    afield = copy.copy(field)
                    for area in to_list(field['domain_name']):
                        domain = domaindef[area]
                        lats = domain.latitudes()
                        afield['latitude'] = { lats[0]:lats[1] }
                        lons = domain.longitudes()
                        afield['longitude'] = { lons[0]:lons[1] }
                        afield['domain_name'] = area
                        record['south'],record['west'],record['north'],record['east'] = domain.coordinates_sn()
                        for level in to_list(field['level']):
                            afield['level'] = level 
                            variables = to_list(field['variable'])
                            for v in variables:
                                afield['variable'] = v
                                for statistic in to_list(field['statistic']):
                                    afield['statistic'] = statistic
                                    for key in record:
                                        if key in field:
                                            record[key] = afield[key]
                                    values = {}
                                    values[v] = f.readArray(afield)
                                    stat = ProdStatistics.create(self.category_,statistic)
                                    stat.compute_raw(values,v,self.storers_,record)
        self.storers_.flush()
                    
prodstat = ProdStat
