import os
import sys
import re
import argparse
from semperpy.core.configure import Configure
from semperpy.core.configfile import ConfigFile
from semperpy.core.tools import no_list
from .dependencies import Dependencies
from .deftable import DefTable
from .deftypes import DefTypes

parser = argparse.ArgumentParser(description='generates the configuration file enabling the Database object to read and write data')
parser.add_argument('--type', choices=['obsstat','score','product'],required = True,help='type of database: obsstat or score')
args = parser.parse_args()
#-----------------------------------------------------------------------------
# Read configuration files, schema definition and other needed parameters.
# Create the driver for that database.
#-----------------------------------------------------------------------------
configure = Configure('semperpy')
db_design = ConfigFile(configure.file('%s_design.def' % args.type[:2],'CONFIG','db/schema'))

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

#-----------------------------------------------------------------------------
# Now go through the tables in ascending order of the number of their
# relations so we make sure they are declared in the right order.
#-----------------------------------------------------------------------------
ta = DefTable()
ty = DefTypes()
for t in tables:
    ta(db_design[t])
    ty(db_design[t])

print(dependency)
print()
print(ta)
print()
print(ty)
