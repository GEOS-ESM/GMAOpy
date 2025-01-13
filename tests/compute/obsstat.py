from gmaopy.modules.obsstat import *

d = obsstat(
    date = Dates(2011030100,2011030200,24),
    domain = ['global','n.hem','s.hem'],
    stats = ['sum','beneficial'],
    type = 'im',
    expver = 'e562p5_fp',
    storage = 'filestorer',
    database = 'obsstat.txt',
    ignore_missing_files = True,
    output_expver = None,
    overwrite = True,
    source = 'oper',
    obs = [
        observation(
            filename = ['summary_all.def'],
            variable = ['xvec'],
        ),
    ],
)
