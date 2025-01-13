from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        type = 'im',
        database = 'im_ops',
        variable = 'xvec',
        domain = ['global'],
        expver = 'e562p5_fp',
        date = Dates(2011030100,2011033100,24),
    ),
    plot = [
        summaryplot(
            plotdata = obsdata(
                statistic = 'impact_per_anl',
                filename = 'summary_all.def',
            ),
        )
    ],
    interactive = False,
    output = 'example7.png',
)
