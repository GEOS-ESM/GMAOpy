from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        type = 'im',
        database = 'im_ops',
        variable = 'xvec',
        domain = ['global'],
        expver = 'e562p5_fp',
        date = Dates(2011030100,2011033100,24),
    ),
    plot = [
        summaryplot(
            plotdata = obsdata(
                filename = 'summary_all.def',
                statistic = ['impact_per_anl'],
            ),
            graphics = graphics(
                bar_color = ['salmon','navy','mistyrose','grey','lightpink','darkred','lightgrey','lightgreen','lightyellow','orange','pink','green','red','cyan','white','orange','black','blue','yellow']
            )
        )
    ],
    interactive = False,
    output = 'example8.png',
)
