from semperpy.db.sqldriver import SQLDriver

class MySQLDriver(SQLDriver):
    
    def write(self,table_name,col_w,col_d,directives,overwrite=False):
        if overwrite:
            self.insert_replace('replace',table_name,col_w,directives)
        else:
            try:
                self.insert_replace('insert',table_name,col_w,directives)
            except self.module().IntegrityError:
                raise self.module().IntegrityError('one of the records to be stored already exists in the database, if you would like to overwrite it use the "overwrite" option')

    def insert_foreign_key(self,id_name,table_name,col_r,col_w,directive):
        old = True
        id = self.find_id(id_name,table_name,col_r,directive)
        if not id:
            old = False
            cursor = self.db_.cursor()
            insert = "insert into %s (" % table_name
            query = insert + self.insert_statement(directive,col_w) + ';'
            #print "foreign key ---->",query
            cursor.execute(query)
            id = self.db_.insert_id()
            cursor.close()
        return id,old
    
    def database(self):
        return 'db'

    def password(self):
        return 'passwd'

    def module(self):
        return MySQLdb

    #----------------------------------------------------------------
    # Schema generation stuff
    #----------------------------------------------------------------
    def index_syntax(self):
        return "alter table <schema>.<table_name> add index (<index>);"

    def auto_increment_syntax(self):
        return 'int not null auto_increment'

    def table_creation_syntax(self):
        return """create table <schema>.<table_name> (\n<columns>\n<unique>\n) engine=myisam;\n<index>\n
        """

class MySQLMissing(object):
    def __init__(self):
        raise SystemError('The module MySQLdb to handle MySQL databases could not be imported. Perhaps it is not installed')

try:
    import MySQLdb
    SQLDriver.registerDriver('mysql',MySQLDriver)
except:
    SQLDriver.registerDriver('mysql',MySQLMissing)
