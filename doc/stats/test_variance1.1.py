from variance1 import Variance
from gmaopy.modules.obsstat import *

obsstat(
    date = Dates(2011030100,2011033100,24),
    domain = ['global'],
    stats = ['unknown'],
    type = 'im',
    expver = 'e562p5_fp',
    database = 'test_obsstat_exp',
    ignore_missing_files = True,
    overwrite = True,
    source = 'oper',
    obs = [
        observation(
            kt = [4,5],
            kx = 220,
            variable = ['xvec'],
        ),
    ],
)
