from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        type = 'im',
        database = 'im_ops',
        variable = 'xvec',
        domain = 'n.hem',
        expver = 'e562p5_fp',
        level = 1000,
        statistic = 'impact_per_anl',
        date = Dates(2011030100,2011033100,24),
    ),
    plot = timeseriesplot(
        curve = line(
            plotdata = obsdata(
                # RaobDsnd
                kx = [120,220,221,132,229,232],
                kt = [4,5,11,44],
            )
        )
    ),
    # we want to generate a file, interactive = True would open a window
    interactive = False,
    output = 'example1.png'
)
