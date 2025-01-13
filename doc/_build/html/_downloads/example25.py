from gmaopy.modules.obsplot import *

document(
    plotdata = odsdata(
        channel = 6,
        type = 'im',
        domain = ['global'],
        expver = 'e562p3_fp',
        date = 2010101300,
        source = 'oper'
    ),
    plot = [
        scatterplot(
            { 'symbol.edgecolor': 'grey', 'graphics.color': 'purple' },
            plotdata = odsdata(
                variable = ['omf','xvec'],
            ),
            curve = curve(
                plotdata = odsdata(
                    kt = 40, kx = 319
                ),
            ),
            xaxis = axis(min = -0.8,max = 0.8),
            yaxis = axis(min = -0.00025,max = 0.00025)
        ),
    ],
    interactive = False,
    output = 'example25.png'
)
