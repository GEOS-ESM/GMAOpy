from semperpy.db.sqldriver import SQLDriver, RollBack
import time

class PGSQLDriver(SQLDriver):

    def write(self,table_name,col_w,col_d,directives,overwrite=False):
        if overwrite:
            try:
                self.delete(table_name,col_d,directives)
                self.insert_replace('insert',table_name,col_w,directives)
            except self.module().InternalError:
                self.db_.rollback()
                raise RollBack()
        else:
            try:
                self.insert_replace('insert',table_name,col_w,directives)
            except self.module().IntegrityError as e:
                raise self.module().IntegrityError(e.message + 'One of the records to be stored already exists in the database, if you would like to overwrite it use the "overwrite" option')
            except self.module().InternalError:
                self.db_.rollback()
                raise RollBack()

    def insert_foreign_key(self,id_name,table_name,col_r,col_w,directive):
        # after trying quite a few different methods, here is the strategy I found to work best to insert
        # new foreign keys without problems with concurrent processes. A unique constraint is set in the
        # database for all the columns for that foreign table. We first check if the id we want is not
        # in a cache or we try to read it from the database if it exists (find_if). If not we try to
        # create it. We try the whole thing three time before failing, waiting for one second after 
        # each failed attempt.
        old = True
        for i in range(3):
            id = self.find_id(id_name,table_name,col_r,directive)
            if id is None:
                old = False
                cursor = self.db_.cursor()
                insert = "insert into %s (" % table_name
                #print "foreign pg---->",insert + self.insert_statement(directive,col_w)
                try:
                    cursor.execute("SELECT nextval('%s_%s_seq')" % (table_name,id_name))
                    row = cursor.fetchone()
                    id = row[0]
                    directive['id'] = id
                    cursor.execute(insert + self.insert_statement(directive,col_w + ['id']))
                    self.db_.commit()
                    return id,old
                except self.module().IntegrityError:
                    time.sleep(1)
                cursor.close()
            else:
                return id,old
        raise self.module().IntegrityError('Could not handle a foreign key for table %s id %s, giving up after three attempts' % (table_name,id_name))

    def module(self):
        return psycopg2

    #----------------------------------------------------------------
    # Schema generation stuff
    #----------------------------------------------------------------
    def index_syntax(self):
        return "create index <table_name>_<index_count>_idx on <schema>.<table_name> (<index>);"

    def table_creation_syntax(self):
        return """create table <schema>.<table_name> (\n<columns>\n<unique>\n);\n<index>\n
        """

    def auto_increment_syntax(self):
        return 'serial'

class PGSQLMissing(object):
    def __init__(self):
        raise SystemError('The module psycopg2 to handle postGreSQL databases could not be imported. Perhaps it is not installed')

try:
    import psycopg2
    import psycopg2.extensions
    SQLDriver.registerDriver('psql',PGSQLDriver)
except:
    SQLDriver.registerDriver('psql',PGSQLMissing)
