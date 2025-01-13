cat > exec.py << EOF
from gmaopy.modules.obsstat import *

d = obsstat(
    # data description
    source = '${py_source}',
    type = 'im',
    expver = '${py_expver}',
    # statistic description
    date = Dates(${py_date_begin},${py_date_end},${py_date_incr}),
    domain = ['global','n.hem','s.hem','tropics'],
    stats = ['sum','beneficial'],
    ignore_missing_files = True,
    # data storage description (database, text file)
    storage =  '${py_storer}',
    database = '${py_store}',
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
            # this file describes all the kx, kt combinations we want to use
            filename = ['summary.def'],
            variable = 'xvec',
        ),
    ],
)
EOF
