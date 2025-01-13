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
            plotdata = odsdata(
                observer = odscounter(varname='total_obs',format='bigNumber')
            ),
            title = [None,None,None,'Total number of observations: <total_obs>'],
            curve = [
                curve(
                    { 'graphics.color': 'lime'},
                    plotdata = odsdata(
                        kt = 44,
                        kx = 120,
                        usage = ['used'],
                        observer = odscounter(varname='total_used',format='bigNumber'),
                    ),
                    legend = '<total_used> used'
                ),
                curve(
                    { 'graphics.color': 'red'},
                    plotdata = odsdata(
                        kt = 44,
                        kx = 120,
                        usage = ['unused'],
                        observer = odscounter(varname='total_rejected',format='bigNumber'),
                    ),
                    legend = '<total_rejected> rejected'
                ),
                curve(
                    { 'graphics.color': 'darkorange' },
                    plotdata = odsdata(
                        kt = 44,
                        kx = 120,
                        usage = ['passive'],
                        observer = odscounter(varname='total_passive',format='bigNumber'),
                    ),
                    legend = '<total_passive> passive'
                ),
            ],
            has_xtitle = False,
            has_legend = True,
            legend = plotlegend(
                mode = None,
                loc = 'outside bottom',
                prop = plotfont(
                    size = 'small'
                ),
                handletextpad = -0.2,
            )
        ),
    ],
    interactive = False,
    output = 'example24.0.png'
)
