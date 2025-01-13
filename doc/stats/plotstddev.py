import stddev
from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        type = 'im',
        variable = 'xvec',
        domain = 'global',
        expver = 'e562p5_fp',
        level = 1000,
        statistic = 'stddev',
        date = Dates(2011030100,2011033100,24),
        database = 'test_obsstat_exp'
    ),
    plot = timeseriesplot(
        curve = line(
            plotdata = obsdata(
                kx = 220,
                kt = [4,5],
            )
        )
    ),
    interactive = False,
    output = 'plotstddev.png'
)
