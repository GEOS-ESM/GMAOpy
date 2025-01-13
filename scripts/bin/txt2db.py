import argparse
from semperpy.core.tools import no_list
from gmaopy.db.dbloader import DBLoader

#-----------------------------------------------------------------------------
# Argument parsing
#-----------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='Populates an SQL database using data from a text file')
parser.add_argument('database',nargs=1,help='name of the database to populate')
parser.add_argument('filename',nargs='+',help='filename(s) of the text files containing data, more than one filename can be specified')
parser.add_argument('--overwrite', action='store_true',default=False,help='overwrites data in the database if already present')
parser.add_argument('--no_check_domains', action='store_false',default=True,help='don\'t check that domain coordinates defined in the text file match those defined in SemperPy')
parser.add_argument('--dry_run', action='store_true',default=False,help='don\'t check that domain coordinates defined in the text file match those defined in SemperPy')
parser.add_argument('--missing_value', type=str,default=None,help='value of missing value if applicable, lines containing missing value are not loaded into the database')
args = parser.parse_args()
args.database = no_list(args.database)

DBLoader(
    files = args.filename,
    database = args.database,
    overwrite = args.overwrite,
    check_domains = args.no_check_domains,
    dry_run = args.dry_run,
    missing_value = args.missing_value)
