from gmaopy.modules.obsplot import *

document(
    plotdata = odsdata(
        type = 'ob',
        domain = ['global'],
        expver = 'e561_tst_02',
        date = 2011020100,
        source = 'oper'   # this is required to be able to find the ODS files
    ),
    plot = [
        coverageplot(
            curve = 
                curve(
                    { 'graphics.color': 'lime'},
                    plotdata = odsdata(
                        kt = 44,
                        kx = 120,
                        usage = ['used'],
                    )
                ),
        ),
    ],
    interactive = False,
    output = 'example21.png'
)
