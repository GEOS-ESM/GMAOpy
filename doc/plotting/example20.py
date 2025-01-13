from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        filename = 'timeseries_acft.def',
        date = Dates(2010090100,2011083100,24),
        type = 'im',
        database = 'im_ops',
        variable = 'xvec',
        domain = ['global'],
    ),
    plot = [
        timeseriesplot(
            plotdata = obsdata(
                statistic = 'impact_per_anl'
            ),
            has_legend = False,
            colormap = colormap(
                min = -0.4,
                max = 0.1,
                step = 0.05,
            ),
            curve = bar(
                plotdata = obsdata(
                    datefile = 'dates.def'
                )
            ),
        ),
    ],
    interactive = False,
    output = 'example20.png',
    size = [11,6]
)
