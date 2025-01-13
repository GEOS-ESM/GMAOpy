from gmaopy.modules.obsplot import *

document(
    plotdata = odsdata(
        type = 'ob',
        domain = ['global'],
        expver = 'e561_tst_02',
        date = Dates(2011020100,2011020100,6),
        source = 'oper'
    ),
    plot = [
        coverageplot(
            curve = 
                curve(
                    { 'graphics.color': 'lime'},
                    plotdata = odsdata(
                        kt = [4,5],
                        kx = 220,
                        usage = ['used'],
                    )
                ),
        ),
    ],
    interactive = False,
    output = 'example22.png'
)
