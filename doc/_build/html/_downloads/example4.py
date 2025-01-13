from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        type = 'im',
        database = 'im_ops',
        variable = 'xvec',
        domain = ['global','n.hem'],  
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
                kt = [4,5,11,44]
            )
        ),
        yaxis = axis(                       # <-
            min = -0.04,                    # <- change
            max = 0.02                      # <-
        ),                                  # <-
        graphics = graphics(                # <-
            linewidth = 3,                  # <- change
            grid = False,                   # <-
        ),                                  # <-
    ),
    layout = [1,2],              
    has_title = True,           
    interactive = False,
    output = 'example4.png',
)
