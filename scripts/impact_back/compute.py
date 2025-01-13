import sys
from gmaopy.modules.obsstat import *

#-----------------------------------------------------------------------------------
# those lines are the price to pay for scripting.... ugly.
#-----------------------------------------------------------------------------------
if len(sys.argv) < 3:
    raise SystemError('expects a directory name and a full path to ODS files')
current =  sys.argv[1]
date,expver,extension = current.split('.')
path = sys.argv[2]
output_file = '%s.%s.stat' % (date,expver)
#-----------------------------------------------------------------------------------

d = obsstat(
    date = date,
    domain = ['global','n.hem','s.hem','tropics'],
    stats = ['sum','beneficial'],
    type = 'im',
    expver = expver,
    ignore_missing_files = True,
    overwrite = True,
    database = 'im_ops',
    source = 'oper',
    # those 3 items tell the system  that the files are in 
    # a path without any subdirectory structure on a disk.
    root_tmpl = path + '/' + current,
    tree_tmpl = '',
    archive_type = 'filesystem',
    obs = [
        observation(
            filename = ['impact.def'],
            variable = 'xvec',
        ),
    ],
)
