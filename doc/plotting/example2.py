from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        type = 'im',
        database = 'im_ops',
        variable = 'xvec',
        domain = ['global','n.hem'],  # <-- the change
        expver = 'e562p5_fp',
        level = 1000,
        levtype = 'pl',
        statistic = 'impact_per_anl',
        date = Dates(2011030100,2011033100,24),
    ),
    plot = timeseriesplot(
        curve = line(
            plotdata = obsdata(
                # RaobDsnd
                kx = [120,220,221,132,229,232],
                kt = [4,5,11,44]
            ),
        )
    ),
    layout = [1,2],               # <-- another change
    has_title = True,             # <-- just one title at document level
    interactive = False,
    output = 'example2.png',
)
