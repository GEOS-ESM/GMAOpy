cat > diag_exec.py << EOF
from gmaopy.modules.obsstat import *

source = '${py_source}'
database = '${py_store}'
expver = '${py_expver}'
dates = Dates(${py_date_begin},${py_date_end},${py_date_incr})
filename = 'obs_compute.def'

obsstat(
    source = source,
    expver = expver,
    domain = ['global','n.hem','s.hem','tropics'],
    date = dates,
    type = 'ob',
    ignore_missing_files = True,
    # data storage description (database, text file)
    database = database,
    storage =  '${py_storer}',
    overwrite = ${py_overwrite},
    # source ODS file description:
    #   - root path
    #   - no tree (all files in directory)
    #   - filesystem, no staging or special actions
    root_tmpl = '${py_location}',
    tree_tmpl = '',
    archive_type = 'filesystem',
    obs = [
        observation(
            variable = ['oma','omf','xvec'],
            statistic = ['count','mean','rms','esigo','esigb','normcost'],
            filename = filename,
            usage = 'used',
        ),
        observation(
            variable = ['oma','omf'],
            statistic = ['count','mean','rms','esigo','esigb'],
            filename = filename,
            usage = 'passive',
        ),
        observation(
            variable = 'oma',
            statistic = 'count',
            filename = filename,
            usage = 'unused',
        ),
    ]
)
EOF
