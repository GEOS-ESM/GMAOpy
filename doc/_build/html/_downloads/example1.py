# imports the needed modules to compute statistics
from gmaopy.modules.obsstat import *

d = obsstat(
    # ODS file description
    source = 'oper',                                           # default
    type = 'ob',
    expver = 'e561_tst_02',
    ignore_missing_files = False,                              # default
    # statistic description
    date = Dates(2011020100,2011020118,6),
    domain = ['global','n.hem','s.hem'],
    statistic = ['count'],
    observation = [
        observation(
            usage = 'used',                                    # default
            variable = ['oma','omf','xvec'],
            statistic = ['count','mean','rms','esigo','esigb','normcost'],
            kx = 220,
            kt = [4,5],
        ),
        observation(
            usage = 'unused',
            variable = 'oma',
            kx = 220,
            kt = [4,5],
        ),
        observation(
            usage = 'passive',
            variable = 'oma',
            kx = 220,
            kt = [4,5],
        ),
    ],
    # data storage description (database, text file)
    storage = 'dbstorer',                                     # default
    database = 'ob_ops',
    overwrite = False,                                        # default
)
