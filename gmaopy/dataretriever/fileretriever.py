import copy
import re
from semperpy.core.tools import no_list, substitute_unix_dates
from semperpy.core.date import Date
from gmaopy.dataretriever.retriever import Retriever
import gmaopy.netcdf

class FileRetriever(Retriever):

    def retrieve(self,directive,indx = None,**kargs):
        dates = list(set(directive['date']))
        dates.sort()
        dates = [ Date(x) for x in dates ]
        url = self.url(directive,'paths',directive['source'],'file')
        config = self.configuration()
        type = directive['type']
        fieldset = []
        reader = self.findReader(directive['source'])
        dir = copy.copy(directive)
        for parameter in directive['parameter']:
            dir['parameter'] = parameter
            if type == 'an':
                for date in dates: 
                    current = substitute_unix_dates(url,'date',date)
                    f = reader(current)
                    dir['date'] = [date.intvalue()]
                    kargs['step'] = 0
                    fs = f.readFieldSet(dir,**kargs)
                    fieldset += fs
            elif type == 'fc':
                for date in dates: 
                    current = substitute_unix_dates(url,'date',date)
                    for step in directive['step']:
                        validD = date + step
                        filename = substitute_unix_dates(current,'valid',validD)
                        f = reader(filename)
                        valid = validD.intvalue()
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
