from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        date = Dates(2011080100,2011083100,24),
        expver = 'e572p1_fp',
        type = 'im',
        database = 'im_ops',
        variable = 'xvec',
        domain = ['global'],
        statistic = 'impact_per_anl',
    ),
    plot = channelplot(
        { 'graphics.grid': False },
        plotdata = obsdata(
            channel = 'all',
        ),
        colormap = colormap(
            min = -0.22,
            max = 0.14,
            step = 0.02,
        ),
        curve = bar(
            plotdata = obsdata(
                # airs
                kx = 49,
                kt = 40
            ),
        ),
    ),
    interactive = False,
    output = 'example19.png'
)
