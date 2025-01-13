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
                filename = 'summary_all.def',
                statistic = ['impact_per_anl'],
            ),
            colormap = colormap(
                min = -0.4,
                max = 0.1,
                step = 0.05,
            ),
        )
    ],
    interactive = False,
    output = 'example10.png',
)
