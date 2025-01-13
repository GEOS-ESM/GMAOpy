from gmaopy.modules.obsplot import *

document(
   plotdata = obsdata(
        type = 'ob',
        database = 'ob_ops',
        expver = 'e572p2_fp',
        date = Dates(2012010100,2012013118,6),
   ),
    plot = [
        levelplot(
            { 
                'graphics.bar_color': ['lime','red'], 'graphics.alpha': 1.0,
                'xaxis.min': 0,
            },
            plotdata = obsdata(
                variable = 'oma',
                statistic = 'count',
                domain = ['global'],
                level = 'all',
                #level = [5.0, 7.0, 10.0, 20.0, 30.0, 50.0, 70.0, 100.0, 150.0, 200.0, 250.0, 300.0, 400.0, 500.0, 700.0, 850.0, 925.0, 1000.0]
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
                )
            ],
            graphics = graphics(
                grid = False
            )
        ),
    ],
    interactive = False,
    output = 'example16.png',
)
