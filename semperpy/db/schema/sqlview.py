import re
from semperpy.core.tools import to_list

class SQLView(object):

    table_names_    = []
    foreign_keys_   = []
    columns_        = []
    view_name_      = 'v_view'

    def __init__(self,driver,schema):
        self.schema_ = schema
        self.driver_ = driver

    def __call__(self,table):
        table_name = table['name_']
        SQLView.table_names_.append('%s.%s' % (self.schema_,table_name))
        if 'foreign_keys_' in table:
            foreign_keys = to_list(table['foreign_keys_'])
            dependencies = to_list(table['dependencies_'])
            if len(foreign_keys) != len(dependencies):    
                raise ValueError('discrepancy between the number of foreign keys and dependencies in table %s: %s,%s' % (table_name,', '.join(foreign_keys), ', '.join(dependencies)))
            for i in range(len(foreign_keys)):
                SQLView.foreign_keys_.append('%s.%s = %s.id' % (table_name,foreign_keys[i],dependencies[i]))
        SQLView.columns_ += [ x for x in table['keys_'] if not re.match('.*id$',x) ]

    def __str__(self):
        create = ''
        create += '\n' + self.driver_.create_view_syntax()
        create = re.sub('<columns>',','.join(self.columns_),create)
        create = re.sub('<where>',' and '.join(self.foreign_keys_),create)
        create = re.sub('<tables>',','.join(self.table_names_),create)
        create = re.sub('<schema>',self.schema_,create)
        create = re.sub('<view>',self.view_name_,create)
        return create
