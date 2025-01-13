from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        type = 'im',
        database = 'im_ops',
        expver = 'e562p5_fp',
        variable = 'xvec',
        domain = 'global',
        statistic = 'impact_per_anl',
        level = 'all',
    ),
    plot = [
        verticalxsection(
            curve = [
                line(
                    plotdata = obsdata(
                        kx = 220,
                        kt = [4,5],
                        date = Dates(2011020100,2011022800,24),
                    ),
                    legend = '<parameter>,Feb'
                ),
                line(
                    plotdata = obsdata(
                        kx = 220,
                        kt = [4,5],
                        date = Dates(2011030100,2011031000,24),
                    ),
                    legend = '<parameter>,Mar'
                ),
            ],
            xtitle = 'Impact',
            title = [None,'',None,None]
        ),
    ],
    layout = [3,1],
    interactive = False,
    output = 'example15.png',
)
