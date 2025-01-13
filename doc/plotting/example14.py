from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        type = 'im',
        database = 'im_ops',
        date = Dates(2011030100,2011033100,24),
        expver = 'e562p5_fp',
        variable = 'xvec',
        domain = 'global',
        statistic = 'impact_per_anl',
        level = 'all',
    ),
    plot = [
        verticalxsection(
            curve = line(
                plotdata = obsdata(
                    kx = 220,
                    kt = 4,
                )
            ),
            xtitle = 'Impact'
        ),
    ],
    layout = [3,1],
    interactive = False,
    output = 'example14.png',
)
