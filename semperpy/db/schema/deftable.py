import re
from semperpy.core.tools import to_list

class DefTable(object):

    table_columns_ = {}
    table_names_ = []

    def __call__(self,table):
        name = table['name_']
        d = DefTable.table_columns_
        r_cols = ','.join([x for x in to_list(table['keys_']) if not re.match('.*id$',x) ])
        d['r_' + name] = r_cols
        DefTable.table_names_.append('r_' + name)
        foreign = to_list(table.get('foreign_keys_',[]))
        d['w_' + name] = r_cols
        if len(foreign) > 0:
            d['w_' + name] += ',' + ','.join(foreign)
        DefTable.table_names_.append('w_' + name)
        if 'delete_' in table:
            d['d_' + name] = ','.join(to_list(table['delete_']))
            DefTable.table_names_.append('d_' + name)

    def __str__(self):
        s = ['[tables]']
        for k in self.table_names_:
            s.append('%s = %s' % (k,self.table_columns_[k]))
        return '\n'.join(s)
