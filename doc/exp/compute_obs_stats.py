from gmaopy.modules.obsstat import *

source = 'exp'
database = 'ob_exp'
expver = 'e572p2_fp'
dates = Dates(2012010100,2012013118,6)
filename = 'obs_compute.def'

d = obsstat(
    source = source,
    database = database,
    expver = expver,
    type = 'ob',
    date = dates,
    domain = ['global','n.hem','s.hem','tropics'],
    ignore_missing_files = True,
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
    ],
)
