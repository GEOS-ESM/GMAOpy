from gmaopy.modules.obsplot import *

domain = ['global']
expver = 'e572p2_fp'
database = 'ob_ops'
dates = Dates(2012010100,2012013118,6)
filename = 'obs_plot_one.def'

document(
    plot = [
        levelplot(
            { 'graphics.bar_color': ['lime','darkorange','red'], 'graphics.alpha': 1.0, 'xaxis.min' : 0, 'yaxis.absolute_max': 8 },
            plotdata = obsdata(
                variable = 'oma',
                statistic = 'count',
                level = 'all',
            ),
            curve = [
                stackedbar(
                    legend = 'used count',
                    plotdata = obsdata(usage = "used")
                ),
                stackedbar(
                    legend = 'passive count',
                    plotdata = obsdata(usage = "passive")
                ),
                stackedbar(
                    legend = 'unused count',
                    plotdata = obsdata(usage = "unused")
                ),
            ],
            graphics = graphics(
                grid = False
            ),
            has_legend = True,
            legend = plotlegend(
                mode = None,
                loc = 'outside top',
                prop = plotfont(
                    size = 'x-small'
                ),
                columnspacing = 0.7,
                handletextpad = 0.7,
            )
        ),
        levelplot(
            { 'graphics.bar_color': ['blue','red','cyan','darkorange'], 'graphics.alpha': 1.0 , 'yaxis.absolute_max': 8},
            plotdata = obsdata(
                statistic = ['rms','mean'],
                level = 'all',
                variable = ['omf','oma'],
                usage = ["used","passive"],
            ),
            graphics = graphics(
                grid = False
            ),
            curve = shiftedbar(legend = '<statistic> <variable>'),
            has_legend = True,
            legend = plotlegend(
                mode = None,
                loc = 'outside top',
                prop = plotfont(
                    size = 'x-small'
                ),
                handletextpad = 0.7,
            )
        ),
        levelplot(
            { 'graphics.bar_color': ['blue','red'], 'graphics.alpha': 1.0, 'xaxis.min' : 0 , 'yaxis.absolute_max': 8},
            plotdata = obsdata(
                statistic = ['normcost'],
                variable = ['omf','oma'],
                level = 'all',
                usage = ["used","passive"],
            ),
            graphics = graphics(
                grid = False
            ),
            curve = shiftedbar(legend = '<statistic> <variable>'),
            has_legend = True,
            legend = plotlegend(
                loc = 'outside top',
                mode = None,
                prop = plotfont(
                    size = 'x-small'
                ),
                handletextpad = 0.7,
            )
        ),
        levelplot(
            { 'graphics.bar_color': ['cyan','blue'], 'graphics.alpha': 1.0, 'xaxis.min' : 0, 'yaxis.absolute_max': 8 },
            plotdata = obsdata(level = 'all'),
            curve = [
                bar(
                    plotdata = obsdata(
                        statistic = 'mean',
                        variable = 'xvec',
                        usage = ["used"],
                    ),
                    legend = '<statistic> sigo'
                ),
                bar(
                    plotdata = obsdata(
                        statistic = 'rms',
                        variable = 'xvec',
                        usage = ["used"],
                    ),
                    legend = '<statistic> sigo'
                ),
                dot(
                    plotdata = obsdata(
                        variable = 'esigo',
                        statistic = 'esigo',
                        usage = ["used","passive"],
                    ),
                    graphics = item(
                        color = 'darkorange',
                        markersize = 8
                    ),
                    legend = '<statistic>'
                   ),
                dot(
                    plotdata = obsdata(
                        variable = 'esigb',
                        statistic = 'esigb',
                        usage = ["used","passive"],
                    ),
                    graphics = item(
                        color = 'black',
                        markersize = 8
                    ),
                    legend = '<statistic>'
                   ),
            ],
            graphics = graphics(
                grid = False
            ),
            has_legend = True,
            legend = plotlegend(
                mode = None,
                loc = 'outside top',
                prop = plotfont(
                    size = 'x-small'
                ),
                handletextpad = 0.7,
            )
        ),
    ],
    plotdata = obsdata(
        domain = domain,
        type = 'ob',
        expver = expver,
        database = database,
        date = dates,
        filename = filename
    ),
    has_title = True,
    title = ['GEOS-5 Observation Monitoring','<name>','<month>','db=<database> expid=<expver>'],
    layout = [2,2],
    size = [10,8],
    interactive = False,
    output = 'overview+<name>.png'
)
