from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        type = 'im',
        database = 'im_ops',
        variable = 'xvec',
        domain = ['global','n.hem'],  # <-- two domains
        expver = 'e562p5_fp',
        level = [1000,500],           # <-- two levels
        statistic = 'impact_per_anl',
        date = Dates(2011030100,2011033100,24),
    ),
    plot = timeseriesplot(
        {
            'graphics.bar_color' : 'khaki'
        },
        curve = bar(
            plotdata = obsdata(
                kx = [120,220,221,132,229,232],
                kt = [4,5,11,44],
            )
        ),
        has_ytitle = False        # <-- not enough room for that
    ),
    layout = [2,2],               # <-- room for more plots
    has_title = True,             
    interactive = False,
    output = 'example5.png',
)
