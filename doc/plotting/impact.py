from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        filename = 'timeseries_all.def',
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
        timeseriesplot(
            plotdata = obsdata(
                statistic = 'impact_per_ob'
            ),
            has_legend = False,
            colormap = colormap(
                min = -1.e-5,
                max = -1.e-8,
                step = (-1.e-8 - -1.e-5) / 2,
            ),
            curve = bar(
                plotdata = obsdata(
                    datefile = 'dates.def'
                ),
            ),
        ),
        timeseriesplot(
            plotdata = obsdata(
                statistic = 'beneficial'
            ),
            has_legend = False,
            colormap = colormap(
                min = 48.0,
                max = 54.0,
                step = 1.0
            ),
            curve = bar(
                plotdata = obsdata(
                    datefile = 'dates.def'
                )
            ),
        )
    ],
    interactive = False,
    output = 'timeseries_<name>_<domain_name>_<statistic>.png',
    size = [11,6]
)
