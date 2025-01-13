from gmaopy.modules.obsstat import *

dates = Dates(1963010100,1963123100,24)

d = obsstat(
    date = dates,
    domain = ['global'],
    statistic = ['count'],
    database = 'ocean',
    source='odas',
    expver = 'ocean',
    #-------------------------------------------------------
    # This is necessary because it will try all combinations
    # 001, 002, 005 etc. for every day
    #-------------------------------------------------------
    ignore_missing_files = True,
    # root_tmpl = 'your path',
    obs = [
    observation(
        type = 'ob',
        variable = ['oma','omf','xvec'],
        statistic = ['count','mean','rms','esigo','esigb','normcost'],
        filename = 'ocean.def',
        ),
    observation(
        type = 'ob',
        usage = 'unused',
        variable = 'oma',
        filename = 'ocean.def',
        ),
    observation(
        type = 'ob',
        usage = 'passive',
        variable = 'oma',
        filename = 'ocean.def',
        ),
    ],
)
