from gmaopy.modules.scoreplot import *

document(
    plotdata = scoredata(
        type = 'fc',
        domain = 'global',
        variable = 'u',
        level = 500,
        levtype = 'pl',
        database = 'fc_ops',
        statistic = ['cor','rms'],
        date = Dates(2012040100,2012043000,24),
        datefile = 'scoredates.def'
    ),
    plot = timeseriesplot(
        { 'graphics.marker' : 'o', 'graphics.markersize': 5 },
        plotdata = scoredata(
            step = [24,48,72,96,120],
        ),
        legend = plotlegend(
            mode = None,
            ncol = 100,
            loc = 'outside top',
            vertical_offset = 0.02,
            prop = plotfont(
                size = 'x-small'
            ),
            columnspacing = 0.7,
            handletextpad = 0.7,
        )
    ),
    interactive = False,
    output = 'score_timeseries_<statistic>.png'
)
