from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        type = 'im',
        database = 'im_ops',
        variable = 'xvec',
        expver = 'e562p5_fp',
        level = 1000,
        statistic = 'impact_per_anl',
        date = Dates(2011030100,2011033100,24),
    ),
    plot = timeseriesplot(
        plotdata = obsdata(
            domain = ['global','n.hem'],  # <-- the change
        ),
        curve = dot(
            plotdata = obsdata(
                # RaobDsnd
                kx = [120,220,221,132,229,232],
                kt = [4,5,11,44]
            )
        )
    ),
    layout = [1,1],               # <-- back to one plot a page
    interactive = False,
    output = 'example3.2.png',
)
