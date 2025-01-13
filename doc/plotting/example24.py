from gmaopy.modules.obsplot import *

document(
    plotdata = odsdata(
        type = 'ob',
        domain = ['global'],
        expver = 'e561_tst_02',
        date = 2011020100,
        source = 'oper'
    ),
    plot = [
        coverageplot(
            { 'symbol.alpha': 0.5 },
            curve = [
                curve(
                    { 'graphics.color': 'lime'},
                    plotdata = odsdata(
                        kt = 44,
                        kx = 120,
                        usage = ['used']
                    )
                ),
                curve(
                    { 'graphics.color': 'red'},
                    plotdata = odsdata(
                        kt = 44,
                        kx = 120,
                        usage = ['unused'],
                    )
                ),
                curve(
                    { 'graphics.color': 'darkorange' },
                    plotdata = odsdata(
                        kt = 44,
                        kx = 120,
                        usage = ['passive'],
                    )
                ),
            ]
        ),
    ],
    interactive = False,
    output = 'example24.png'
)
