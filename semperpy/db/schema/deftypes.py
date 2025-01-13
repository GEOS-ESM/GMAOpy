import re
from semperpy.core.tools import to_list

class DefTypes(object):

    types_ = {}

    def __call__(self,table):
        keys = [x for x in to_list(table['keys_']) if not re.match('.*id$',x) ]
        for key in keys:
            if key in DefTypes.types_:
                raise ValueError('Column names should be unique even across tables: %s',key)
            DefTypes.types_[key] = self.pythonType(table[key])

    def pythonType(self,t):
        t = t.split(' ')[0]
        if re.match('varchar',t):
            return 'str'
        return t

    def __str__(self):
        keys = list(self.types_.keys())
        keys.sort()
        types = ['[types]']
        for key in keys:
            types.append('%s = %s' % (key,self.types_[key]))
        return '\n'.join(types)
