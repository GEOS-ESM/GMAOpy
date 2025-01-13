from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        domain = ['global'],
        type = 'ob',
        database = 'ob_ops',
        expver = 'e572p2_fp',
        date = Dates(2012010100,2012013118,6),
    ),
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
                    plotdata = obsdata(
                        usage = "used",
                        kx = 220,
                        kt = [4,5]
                    )
                ),
                stackedbar(
                    plotdata = obsdata(
                        usage = "passive",
                        kx = 220,
                        kt = [4,5]
                    )
                ),
                stackedbar(
                    plotdata = obsdata(
                        usage = "unused",
                        kx = 220,
                        kt = [4,5]
                    )
                )
            ],
            graphics = graphics(
                grid = False
            )
        ),
        levelplot(
            { 'graphics.bar_color': ['blue','red','cyan','darkorange'], 'graphics.alpha': 1.0 , 'yaxis.absolute_max': 8},
            plotdata = obsdata(
                statistic = ['rms','mean'],
                level = 'all',
                usage = ["used","passive"],
                variable = ['omf','oma'],
            ),
            graphics = graphics(
                grid = False
            ),
            curve = shiftedbar(
                plotdata = obsdata(
                    kx = 220,
                    kt = [4,5]
                )
            )
        ),
        levelplot(
            { 'graphics.bar_color': ['blue','red'], 'graphics.alpha': 1.0, 'xaxis.min' : 0 , 'yaxis.absolute_max': 8},
            plotdata = obsdata(
                statistic = ['normcost'],
                variable = ['omf','oma'],
                usage = ["used","passive"],
                level = 'all',
            ),
            graphics = graphics(
                grid = False
            ),
            curve = shiftedbar(
                plotdata = obsdata(
                    kx = 220,
                    kt = [4,5]
                )
            )
        ),
        levelplot(
            { 'graphics.bar_color': ['cyan','blue'], 'graphics.alpha': 1.0, 'xaxis.min' : 0, 'yaxis.absolute_max': 8 },
            plotdata = obsdata(
                level = 'all',
            ),
            curve = [
                bar(
                    plotdata = obsdata(
                        statistic = 'mean',
                        variable = 'xvec',
                        kx = 220,
                        kt = [4,5]
                    )
                ),
                bar(
                    plotdata = obsdata(
                        statistic = 'rms',
                        variable = 'xvec',
                        kx = 220,
                        kt = [4,5]
                    )
                ),
                dot(
                    plotdata = obsdata(
                        variable = 'esigo',
                        statistic = 'esigo',
                        usage = ["used","passive"],
                        kx = 220,
                        kt = [4,5],
                    ),
                    graphics = item(
                        color = 'darkorange',
                        markersize = 8
                    )
                   ),
                dot(
                    plotdata = obsdata(
                        variable = 'esigb',
                        statistic = 'esigb',
                        usage = ["used","passive"],
                        kx = 220,
                        kt = [4,5],
                    ),
                    graphics = item(
                        color = 'black',
                        markersize = 8
                    )
                   ),
            ],
            graphics = graphics(
                grid = False
            )
        ),
    ],
    layout = [2,2],
    size = [10,7],
    has_title = True,
    title = ['GEOS-5 Observation Monitoring','<name>','<month>'],
    interactive = False,
    output = 'example18.png'
)
