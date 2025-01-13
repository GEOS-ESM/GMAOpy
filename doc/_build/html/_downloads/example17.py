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
            { 'graphics.bar_color': ['red','blue','gold','cyan'], 'graphics.alpha': 1.0 },
            plotdata = obsdata(
                statistic = ['normcost'],
                variable = ['oma','omf'],
                domain = ['global'],
                level = 'all',
            ),
            graphics = graphics(
                grid = False
            ),
            curve = shiftedbar(
                plotdata = obsdata(
                    kx = 220,
                    kt = [4,5],
                ),
            )
        ),
    ],
    interactive = False,
    output = 'example17.png'
)
