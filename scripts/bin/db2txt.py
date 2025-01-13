import sys
import argparse
from semperpy.core.tools import no_list
from gmaopy.modules.dbdump import *
from gmaopy.db.database import Database

def intList(what):
    if what is None:
        return None
    l = what.split(',')
    return [ int(x) for x in l ]

def floatList(what):
    if what is None:
        return None
    l = what.split(',')
    return [ float(x) for x in l ]

def strList(what):
    if what is None:
        return None
    return what.split(',')

#-----------------------------------------------------------------------------
# Argument parsing
#-----------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='Dump the whole contents or part of an SQL database into a text file. Please not that not all keywords are valid for all databases, support is provided, if a wrong keyword is specified')
parser.add_argument('database',nargs=1,help='name of the database to dump')
parser.add_argument('filename',nargs=1,help='filename of the text file to create')
parser.add_argument('--begindate', type=int,default=None,help='start date in the form YYYYMMDDHH')
parser.add_argument('--enddate', type=int,default=None,help='end date in the form YYYYMMDDHH')
parser.add_argument('--expver', default=None,help='experiment ID of the data to dump')
parser.add_argument('--level', type=str,default=None,help='list of pressure level to dump')
parser.add_argument('--kx', type=str,default=None,help='list of kx')
parser.add_argument('--kt', type=str,default=None,help='list of kt')
parser.add_argument('--domain_name', type=str,default=None,help='name of a geographical area')
parser.add_argument('--statistic', type=str,default=None,help='name of a (raw) statistic')
parser.add_argument('--usage', choices=['used','passive','rejected'],default=None,help='data usage flag')
parser.add_argument('--variable', type=str,default=None,help='name of a variable')
parser.add_argument('--append', action='store_true',default=False,help='if the file exists, append data to the file')
args = parser.parse_args()

args.kx = intList(args.kx)
args.kt = intList(args.kt)
args.level = floatList(args.level)
args.filename = no_list(args.filename)
args.database = no_list(args.database)

db = Database(args.database,write = False)
info = db.dbInfo(args.database)
record_name = info['recordtype']
record = db.createDBGenericRecord(record_name)
language = set(record.keys())
extra = set(['begindate','enddate','database','filename','append'])
args = vars(args)
directive_args = {}
for k,i in list(args.items()):
    if i is not None:
        if not k in language and not k in extra:
            sys.stderr.write("Keyword %s is not valid for database %s of type %s\n\n" % (k,args['database'],record_name))
            exit(1)
        directive_args[k] = i

dbdump(**directive_args)
