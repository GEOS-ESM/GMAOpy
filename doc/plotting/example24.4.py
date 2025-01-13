from gmaopy.modules.obsplot import *

document(
    plotdata = odsdata(
        type = 'ob',
        domain = ['n.hem'],
        expver = 'e561_tst_02',
        date = 2011020100,
        source = 'oper'   # this is required to be able to find the ODS files
    ),
    plot = [
        coverageplot(
            plotdata = odsdata(
                variable = 'omf'
            ),
            geography = geography(
                projection = 'stere',
                lon_0 = 270,
                hemisphere = 'north',
                south = 50,
                plot_over = ["coastlines","parallels","meridians"]
            ),
            curve = 
                curve(
                    plotdata = odsdata(
                        kt = 44,
                        kx = 120,
                        usage = ['used'],
                    )
                ),
        ),
    ],
    interactive = False,
    output = 'example24.4.png'
)
