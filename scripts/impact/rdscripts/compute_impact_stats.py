from gmaopy.modules.obsstat import *

source = 'exp'
database = 'im_exp'
expver = 'e561_tst_02'
dates = Dates(2012010100,2012013100,24)
filename = 'summary_all.def'

d = obsstat(
    source = source,
    database = database,
    expver = expver,
    type = 'im',
    date = dates,
    domain = ['global','n.hem','s.hem','tropics'],
    ignore_missing_files = True,
    statistic = ['sum','beneficial'],
    obs = [
        observation(
            filename = ['summary_all.def'],
            variable = ['xvec'],
        ),
    ],
)
