from gmaopy.modules.obsstat import *

d = obsstat(
    date = Dates(2011020100,2011020118,6),
    overwrite = True,
    domain = ['global','n.hem','s.hem'],
    statistic = ['count'],
    storage = 'filestorer',
    database = 'wind.txt',
    expver = 'e561_tst_02',
    source = 'oper',
    obs = [
    observation(
        type = 'ob',
        variable = ['oma','omf','xvec'],
        statistic = ['mean','rms','esigo','esigb','normcost'],
        kx = 220,
        kt = [4,5],
        ),
    observation(
        type = 'ob',
        usage = 'unused',
        variable = 'oma',
        kx = 220,
        kt = [4,5],
        ),
    observation(
        type = 'ob',
        usage = 'passive',
        variable = 'oma',
        kx = 220,
        kt = [4,5],
        ),
    ]
)
