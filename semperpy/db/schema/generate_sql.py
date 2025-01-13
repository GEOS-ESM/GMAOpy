import os
import sys
import argparse
import re
from semperpy.core.configure import Configure
from semperpy.core.configfile import ConfigFile
from semperpy.core.tools import no_list,to_list
from semperpy.db.sqldriver import SQLDriver
from .dependencies import Dependencies
from .sqltable import SQLTable
from .sqlview import SQLView

#-----------------------------------------------------------------------------
# Argument parsing
#-----------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='generates the SQL instructions to create a logical database')
parser.add_argument('database',nargs=1,help='name of the database to be created')
parser.add_argument('--drop', action='store_true',default=False,help='drop the database if it already exists')
parser.add_argument('--drop_only', action='store_true',default=False,help='drop the database if it already exists and does nothing else')
parser.add_argument('--grant_only', action='store_true',default=False,help='only generate the sql GRANT instructions')
args = parser.parse_args()
args.database = no_list(args.database)

#-----------------------------------------------------------------------------
# Read configuration files, schema definition and other needed parameters.
# Create the driver for that database.
#-----------------------------------------------------------------------------
configure = Configure('semperpy')
loc = configure.localise()
databases = ConfigFile(configure.file('databases%s.def' % loc,'CONFIG','db'))
if not args.database in databases:
    raise ValueError('Database %s is not defined in the database configuration file' % args.database)
database = databases[args.database]
db_design = ConfigFile(configure.file('%s_design.def' % database['recordtype'][:2],'CONFIG','db/schema'))
driver = SQLDriver.createDriver(database['engine'])

#-----------------------------------------------------------------------------
# Go through the tables to determine dependencies and the order in which we
# should process the tables
#-----------------------------------------------------------------------------
dependency = Dependencies()
for table in list(db_design.values()):
    dependencies = []
    if 'dependencies_' in table:
        dependencies = table['dependencies_']
    dependency(table['name_'],dependencies)
tables = dependency.ordered()

if not args.grant_only:
    #-----------------------------------------------------------------------------
    # Now go through the tables in ascending order of the number of their
    # relations so we make sure they are declared in the right order.
    #-----------------------------------------------------------------------------
    schema = []
    if args.drop or args.drop_only:
        if 'protected' in database and database['protected'].lower() == 'yes':
            sys.stderr.write('The database %s is protected, please ask a SemperPy administrator to delete it\n\n' % args.database)
            exit(1)
        sys.stderr.write('This will delete the data in database %s permanently, are you sure? y/n [n]: ' % args.database)
        r = input()
        if r == 'y' or r == 'Y':
            schema.append(re.sub('<schema>',args.database,driver.drop_schema_syntax()))
            if args.drop_only:
                print('\n'.join(schema),'\n')
                exit(0)
        else:
            exit(1)
    schema.append(re.sub('<schema>',args.database,driver.create_schema_syntax()))
    print('\n'.join(schema),'\n')
    view = SQLView(driver,args.database)
    for t in tables:
        table = SQLTable(args.database,driver,db_design[t])
        print(table) 
        view(db_design[t])
    print(view)
    print()

#-----------------------------------------------------------------------------
# Now grant access to users
#-----------------------------------------------------------------------------
users = to_list(database['userr'])
if 'grantr' in database:
    users = to_list(database['grantr'])
for user in users:
    print("grant usage on schema %s to %s;" % (args.database,user))
    for table in tables:
        print("grant select on table %s.%s to %s;" % (args.database,table,user)) 
    print("grant select on table %s.%s to %s;" % (args.database,SQLView.view_name_,user))
    print()
