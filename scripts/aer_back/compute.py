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
#-----------------------------------------------------------------------------------

obsstat(
    date = date,
    domain = ['global','n.hem','s.hem','tropics'],
    database = 'ob_ops',
    type = 'ob',
    source = 'aer',
    expver = expver,
    ignore_missing_files = True,
    overwrite = False,
    statistic = 'count',
    # those 3 items tell the system  that the files are in 
    # a path without any subdirectory structure on a disk.
    root_tmpl = path + '/' + current,
    tree_tmpl = '',
    archive_type = 'filesystem',
    obs = [
        observation(
            variable = ['oma','omf','xvec'],
            statistic = ['count','mean','rms','esigo','esigb','normcost'],
            filename = 'aer.def'
            ),
        observation(
            usage = 'unused',
            variable = 'oma',
            statistic = 'count',
            filename = 'aer.def'
            ),
        observation(
            usage = 'passive',
            variable = ['oma','omf'],
            statistic = ['count','mean','rms','esigo','esigb'],
            filename = 'aer.def'
            ),
    ]
)
