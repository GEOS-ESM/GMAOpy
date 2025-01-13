import copy
import re
from semperpy.core.tools import no_list, substitute_unix_dates
from semperpy.core.date import Date
from semperpy.netcdf.file import File
from gmaopy.dataretriever.retriever import Retriever
import gmaopy.netcdf

class DAPRetriever(Retriever):

    def retrieve(self,directive,indx = None,**kargs):
        url = self.url(directive,'servers',directive['source'],'dap')
        config = self.configuration()
        dates = list(set(directive['date']))
        dates.sort()
        dates = [ Date(x) for x in dates ]
        type = directive['type']
        fieldset = []
        dir = copy.copy(directive)
        for parameter in directive['parameter']:
            dir['parameter'] = parameter
            if type == 'an':
                f = File(url)
                for date in dates: 
                    dir['date'] = [date.intvalue()]
                    kargs['step'] = 0
                    fs = f.readFieldSet(dir,**kargs)
                    fieldset += fs
            elif type == 'fc':
                for date in dates: 
                    current = substitute_unix_dates(url,'date',date)
                    f = File(current)
                    for step in directive['step']:
                        valid = (date + step).intvalue()
                        dir['date'] = [valid]
                        kargs['step'] = step
                        fs = f.readFieldSet(dir,**kargs)
                        for field in fs:
                            field.set('date',date.intvalue())
                            field.set('valid_date',valid)
                        fieldset += fs
            else:
                raise ValueError('Unknown type %s' % (type))
        return fieldset
