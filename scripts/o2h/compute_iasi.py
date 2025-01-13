from gmaopy.modules.obsstat import *
import sys

source = 'oper'
database = 'ob_ops'
expver = sys.argv[3]
dates = Dates(sys.argv[1],sys.argv[2],6)
filename = 'iasi.def'

d = obsstat(
    source = source,
    database = database,
    expver = expver,
    overwrite = True,
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
            variable = 'omf',
            statistic = 'count',
            filename = filename,
            usage = 'unused',
        ),
    ]
)
