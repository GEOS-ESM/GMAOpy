# imports the needed modules to compute statistics
from gmaopy.modules.obsstat import *

obsstat(
    # ODS file  description
    source = 'oper',                                   # default
    type = 'im',
    expver = 'e562p5_fp',
    ignore_missing_files = True,
    # statistic description
    date = Dates(2011030100,2011030200,24),
    domain = ['global','n.hem','s.hem','tropics'],
    statistic = ['sum','beneficial'],
    # data storage description (database, text file)
    storage =  'dbstorer',                             # default
    database = 'im_ops',
    overwrite = False,                                 # default
    obs = [
        observation(
            # this file describes all the kx, kt combinations we want to use
            filename = ['summary.def'],
            variable = 'xvec',
        ),
    ],
)
