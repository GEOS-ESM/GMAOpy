import re
from semperpy.core.tools import to_list

class SQLTable(object):
    
    index_count_ = 0

    def __init__(self,schema,driver,table):
        columns = []
        for key in ['keys_','foreign_keys_']:
            columns += self.columns(table,key)
        columns = ',\n'.join(columns)
        columns = re.sub('<auto_increment>',driver.auto_increment_syntax(),columns)
        index = []
        key = 'index_'
        template = driver.index_syntax()
        if key in table:
            for indx in to_list(table[key]):
                index.append(re.sub('<index>',indx,template))
        key = 'composite_index_'
        if key in table:
            index.append(re.sub('<index>',','.join(to_list(table[key])),template))
        key = 'composite_primary_'
        if key in table:
            index.append(re.sub('<key>',','.join(to_list(table[key])),driver.primary_key_syntax()))
        index = '\n'.join(index)
        indices = re.findall('<index_count>',index)
        for i in range(len(indices)):
            index = re.sub('<index_count>',str(self.index_count_),index,1)
            SQLTable.index_count_ += 1
        result = driver.table_creation_syntax()
        unique=''
        if 'unique' in table:
            unique = driver.unique_syntax(table['unique']) + '\n'
        if len(unique) > 0:
            columns += ','
        result = re.sub('<columns>',columns,result)
        result = re.sub('<unique>\n',unique,result)
        result = re.sub('<index>',index,result)
        result = re.sub('<table_name>',table['name_'],result)
        result = re.sub('<schema>',schema,result)
        self.text_ = result
    

    def columns(self,table,key):
        columns = []
        if key in table:
            keys = to_list(table[key])
            for key in keys:
                columns.append(key + ' ' + table[key])
        return columns

    def __str__(self):
        return self.text_
