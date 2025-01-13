from gmaopy.modules.scoreplot import *

document(
    plotdata = scoredata(
        type = 'fc',
        domain = 'global',
        variable = 't',
        level = 500,
        levtype = 'pl',
        statistic = ['rms','cor'],
        database = 'fc_ops', 
        date = Dates(2012040100,2012043000,24),
    ),
    title = [' ','<level> <variable> <domain_name>'],
    plot = [ 
      diffplot(
        { 'graphics.marker' : 'o', 'graphics.markersize': 5 },
        plotdata = scoredata(
            step = [0,6,12,18,24,30,36,42,48,54,60,66,72,78,84,90,96,102,108,114,120],
        ),
        legend = plotlegend(
            ncols = 5,
            loc = 'outside top',
            mode = None,
            prop = plotfont(
                size = 'x-small'
            )
        ),
        curve = [
            line(
                graphics = graphics(color = 'black',marker = ''),
                plotdata = scoredata(forecast = 'gmao',verify = 'gmao'),
                legend = 'e572p5_fp (<population>)',
            ),
            line(
                graphics = graphics(color = 'darkturquoise'),
                plotdata = scoredata(forecast = 'ecmwf',verify = 'ecmwf'),
                legend = 'ECMWF (<population>)'
            ),
            line(
                graphics = graphics(color = 'blue'),
                plotdata = scoredata(forecast = 'ncep',verify = 'ncep'),
                legend = 'NCEP (<population>)',
            ),
            line(
                graphics = graphics(color = 'green'),
                plotdata = scoredata(forecast = 'gmao',verify = 'ecmwf'),
                legend = 'g5ecmwf (<population>)'
            ),
            line(
                graphics = graphics(color = 'red'),
                plotdata = scoredata(forecast = 'gmao',verify = 'ncep'),
                legend = 'g5ncep (<population>)'
            ),
        ],
        has_xtitle = True,
        xtitle = 'Forecast Day (<month>)',
        has_ytitle = True,
        ytitle = 'Difference (ref=GEOS-5)',
      ),
    ],
    interactive = False,
    output = 'diff_<statistic>.png',
    layout = [1,2],
    size = [9,7],
    has_title = True
)
