from collections import defaultdict
from semperpy.core.factory import Factory
from semperpy.core.decorators import abstractMethod
from semperpy.core.tools import is_list, is_tuple_or_list, is_string, to_list, is_dict

class RollBack(Exception):
    pass

class SQLDriver(object):

    class DeleteError(Exception):
        pass

    drivers_ = Factory()
    keywords_ = frozenset(['port','host','database','user','password'])

    def __init__(self):
        self.id_cache_ = defaultdict(dict)

    def __getattr__(self,attribute):
        if attribute in self.keywords_:
            return attribute
        return super(SQLDriver,self).__getattr__(attribute)

    def connect(self,**kargs):
        arguments = {}
        for key in self.keywords_:
            if key in kargs:
                arguments[getattr(self,key)] = kargs[key]
        #print arguments
        self.db_ = self.module().connect(**arguments)

    def close(self):
        self.db_.close()

    def cursor(self):
        return self.db_.cursor()

    def executeQuery(self,cursor,query,result,keys,retrieve_keys,value_col):
        cursor.execute(query)
        while True:
            row = cursor.fetchone()
            if not row:
                break
            k = 0
            for ret in retrieve_keys:
                d = {}
                j = 0
                for key in keys:
                    d[key] = row[j]
                    j += 1
                values = row[len(keys) + k]
                if to_list(values)>0:
                    d[ret] = to_list(values)
                    result[ret].store(d,ret)
                k += 1

    def select_statement(self,directive,key_list,negated=[]):
        query = []
        for key in key_list:
            if key in directive:
                item = directive[key]
                negate = ''
                if key in negated:
                    negate = 'not '
                if is_dict(item):
                    beg = list(item.keys())[0]
                    begin = str(beg)
                    end = str(item[beg])
                    if negate == '':
                        query.append('%s >= %s and %s < %s' % (key,begin,key,end))
                    else:
                        query.append('%s < %s and %s >= %s' % (key,begin,key,end))
                elif is_tuple_or_list(item):
                    if is_string(item[0]):
                        query.append('%s%s in (%s)' % (negate,key,','.join([ "'"+x+"'" for x in item])))
                    else:
                        #if 'date' in key:
                            #for date in item:
                            #    query.append('%s%s >= %s and %s < %s' % (negate,key,date[0],key, date[-1]))
                        #    query.append('%s%s >= %s and %s < %s' % (negate,key,item[0][0],key, item[0][-1])) # ','.join([ str(x) for x in item])))
                            #query.append('%s%s in (%s)' % (negate,key,','.join([ str(x) for x in item[0]])))
                        #else:
                        query.append('%s%s in (%s)' % (negate,key,','.join([ str(x) for x in item])))
                elif is_string(item):
                    query.append("(%s%s = '%s')" % (negate,key,item))
                else:
                    query.append('(%s%s = %s)' % (negate,key,str(item)))
        return ' AND '.join(query)

    def insert_statement(self,directive,key_list,valuesOnly = False):
        keys = []
        values = []
        for key in key_list:
            item = directive[key]
            if not valuesOnly:
                keys.append(key)
            if is_list(item):
                item = item[0]
            elif is_string(item):
                item = "'" + item + "'"    
            item = str(item)
            values.append(item)
        if valuesOnly:
            return "(" + ','.join(values) + ")"
        else:
            return ','.join(keys) + ") values (" + ','.join(values) + ")"

    def find_id(self,id_name,table_name,table_columns,directive):
        return self.find_all_id(id_name,table_name,table_columns,directive,first = True)

    def find_all_id(self,id_name,table_name,table_columns,directive,first = False):
        name = ''.join([ str(directive[x]) for x in table_columns ])
        if name in self.id_cache_[table_name]:
            return self.id_cache_[table_name][name]
        cursor = self.db_.cursor()
        select = "select %s from %s where " % (id_name, table_name)
        query = select + self.select_statement(directive,table_columns) + ';'
        cursor.execute(query)
        row = cursor.fetchall()
        #print "find_id--->",query,row 
        cursor.close()
        if row and len(row) > 0:
            if first:
                id = row[0][0]
                #print "id found",table_name
                self.id_cache_[table_name][name] = id
                return id
            else:
                return [ x[0] for x in row]
        #print "id not found",table_name
        return None

    def insert_replace(self,what,table_name,col_w,directives):
        command = "%s into %s (" % (what,table_name)
        rows = []
        values_only = False
        for directive in directives:
            sql = self.insert_statement(directive,col_w,values_only)
            rows.append(sql)
            values_only = True
        cursor = self.db_.cursor()
        #print '%s %s;' % (command,','.join(rows))
        cursor.execute('SELECT version();')
        print((cursor.fetchone()))
#        print('*****TEST*****', rows.count('nan'))
        for x in range(rows.count('nan')):
            rows.remove('nan')
        cursor.execute("%s %s;" % (command,','.join(rows)))
        cursor.close()

    def delete(self,table_name,col_d,directives):
        command = "delete from %s where " % table_name
        cursor = self.db_.cursor()
        for d in directives:
            sql = command + self.select_statement(d,col_d) + ';'
            #print sql
            cursor.execute(sql)
        cursor.close()

    def delete_id(self,table_name,columns,directive,dryrun=False):
        if len(columns) == 0:
            return
        command = "delete from %s where " % table_name
        cursor = self.db_.cursor()
        sql = command + self.select_statement(directive,columns) + ';'
        try:
            if dryrun:
                print(sql)
            else:
                cursor.execute(sql)
            cursor.close()
        except:
            raise SQLDriver.DeleteError()

    def begin_transaction(self):
        c = self.db_.cursor()
        c.execute("begin")
        c.close()

    def end_transaction(self):
        self.db_.commit()

    #----------------------------------------------------------------
    # Abstract methods
    #----------------------------------------------------------------
    @abstractMethod
    def module(self):
        pass

    @abstractMethod
    def write(self,table_name,col_w,col_d,directives,overwrite=False):
        pass

    @abstractMethod
    def insert_foreign_key(self,id_name,table_name,col_r,col_w,directive):
        pass

    @abstractMethod
    def auto_increment_syntax(self):
        pass

    @abstractMethod
    def index_syntax(self):
        pass

    @abstractMethod
    def table_creation_syntax(self):
        pass
    #----------------------------------------------------------------
    # Class methods
    #----------------------------------------------------------------
    @classmethod
    def registerDriver(self,what,driver):
        self.drivers_.register(what,driver)

    @classmethod
    def createDriver(self,what,*args,**kargs):
        return self.drivers_.create(what,*args,**kargs)

    #----------------------------------------------------------------
    # Schema generation utilities
    #----------------------------------------------------------------
    def primary_key_syntax(self):
        return "alter table <schema>.<table_name> add primary key (<key>);"

    def create_view_syntax(self):
        return "create or replace view <schema>.<view> (<columns>)\nas select <columns>\nfrom <tables> where <where>;"

    def create_schema_syntax(self):
        return "create schema <schema>;"

    def drop_schema_syntax(self):
        return "drop schema <schema> cascade;"

    def unique_syntax(self,keys):
        keys = to_list(keys)
        return "unique (%s)" % ','.join(keys)
