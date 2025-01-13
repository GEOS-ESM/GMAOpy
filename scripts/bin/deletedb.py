import sys
import argparse
from semperpy.core.tools import no_list
from semperpy.core.date import Dates
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
parser = argparse.ArgumentParser(description='Delete selected statistics. Please not that not all keywords are valid for all databases, support is provided, if a wrong keyword is specified')
parser.add_argument('database',nargs=1,help='name of the database to delete data from')
parser.add_argument('--begindate', type=int,default=None,help='start date in the form YYYYMMDDHH')
parser.add_argument('--enddate', type=int,default=None,help='end date in the form YYYYMMDDHH')
parser.add_argument('--expver', default=None,help='experiment ID of the data to dump')
parser.add_argument('--level', type=str,default=None,help='list of pressure level to dump')
parser.add_argument('--kx', type=str,default=None,help='list of kx')
parser.add_argument('--kt', type=str,default=None,help='list of kt')
parser.add_argument('--domain_name', type=str,default=None,help='name of a geographical area')
parser.add_argument('--statistic', type=str,default=None,help='name of a statistic')
parser.add_argument('--usage', choices=['used','passive','rejected'],default=None,help='data usage flag')
parser.add_argument('--variable', type=str,default=None,help='name of a variable')
parser.add_argument('--dryrun', action='store_true',default=False,help='only displays sql commands without executing them')
args = parser.parse_args()

args.kx = intList(args.kx)
args.kt = intList(args.kt)
args.level = floatList(args.level)
args.database = no_list(args.database)

db = Database(args.database,write = True)
info = db.dbInfo(args.database)
record_name = info['recordtype']
record = db.createDBGenericRecord(record_name)
language = set(record.keys())
args = vars(args)
if args['begindate'] is not None and args['enddate'] is not None:
    args['date'] = Dates(args['begindate'],args['enddate'],24)
del args['begindate']
del args['enddate']
extra = ['database','dryrun']
directive_args = {}
for k,i in list(args.items()):
    if i is not None:
        if not k in language:
            if not k in extra:
                sys.stderr.write("Keyword %s is not valid for database %s of type %s\n\n" % (k,args['database'],record_name))
                exit(1)
        else:
            directive_args[k] = i

if len(directive_args) == 0:
    sys.stderr.write('Empty request, cowardly refusing to delete anything\n')     
    exit(1)
if 'protected' in info and info['protected'].lower() == 'yes':
    sys.stderr.write('The database %s is protected, are you sure you want to delete data? y/n [n]: ' % args['database'])
    r = input()
    if r != 'y' and r != 'Y':
        sys.stderr.write('The delete command was cancelled\n')
        exit(1)
sys.stderr.write('Deleting...\n')
sys.stderr.write(str(directive_args))
sys.stderr.write('\n')
db.delete(directive_args,dryrun = args['dryrun'])
