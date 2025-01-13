from gmaopy.modules.obsplot import *

expver = 'e572p2_fp'
database = 'ob_exp'
dates = Dates(2012010100,2012013118,6)
filename = 'obs_plot.def'
domain = ['global']

document(
    plot = [
        timeseriesplot(
            { 
                'graphics.bar_color': ['lime','darkorange','red'],
                'graphics.alpha': 1.0,
                'graphics.bar_width_factor': 1,
                'graphics.automatic_edge': False,
            },
            plotdata = obsdata(
                statistic = 'count',
                variable = 'oma',
            ),
            legend = plotlegend(
                columnspacing = 0.7,
                handletextpad = 0.7,
                location = 'outside top',
                mode = None,
                prop = plotfont(
                    size = 'x-small'
                )
            ),
            has_ytitle = False,
            curve = [
                stackedbar(
                    plotdata = obsdata(usage = 'used'),
                    legend = 'used obs count'
                ),
                stackedbar(
                    plotdata = obsdata(usage = 'passive'),
                    legend = 'passive obs count'
                ),
                stackedbar(
                    plotdata = obsdata(usage = 'unused'),
                    legend = 'unused obs count'
                )
            ]
        ),
        timeseriesplot(
            { 
                'graphics.bar_color': ['red','blue','gold','cyan'], 
                'graphics.alpha': 1.0,
                'graphics.bar_width_factor': 1,
                'graphics.automatic_edge': False,
            },
            plotdata = obsdata(
                statistic = ['rms','mean'],
                variable = ['oma','omf'],
            ),
            legend = plotlegend(
                columnspacing = 0.7,
                handletextpad = 0.7,
                location = 'outside top',
                mode = None,
                prop = plotfont(
                    size = 'x-small'
                )
            ),
            has_ytitle = False,
            curve = [
                bar(
                    plotdata = obsdata(usage = ['used','passive']),
                    legend = '<statistic> <variable>'
                ),
            ],
            has_title = False,
        ),
        timeseriesplot(
            { 
                'graphics.bar_color': ['red','blue'],
                'graphics.alpha': 1.0,
                'graphics.bar_width_factor': 1,
                'graphics.automatic_edge': False,
            },
            plotdata = obsdata(
                statistic = ['normcost'],
                variable = ['oma','omf'],
            ),
            legend = plotlegend(
                columnspacing = 0.7,
                handletextpad = 0.7,
                location = 'outside top',
                mode = None,
                prop = plotfont(
                    size = 'x-small'
                )
            ),
            has_ytitle = False,
            curve = [
                bar(
                    plotdata = obsdata(usage = 'used'),
                    legend = '<statistic> <variable>'
                ),
            ],
            has_title = False
        ),
    ],
    plotdata = obsdata(
        type = 'ob',
        expver = expver,
        database = database,
        filename = filename,
        date = dates,
        domain = domain,
        level = 'all',
    ),
    layout = [1,3],
    has_title = True,
    title = [None,'<month>',None,'<name>','db=<database> expid=<expver>'],
    size = [11,7],
    interactive = False,
    output = 'timeseries_obs+<level>+<name>.png'
)
