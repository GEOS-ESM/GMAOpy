from semperpy.core.date import date
from gmaopy.modules.obsplot import *

expver          = 'e572p2_fp'
database        = 'im_ops'
option          = 'all'

begin = Date(2012032900)
end = 2012033100

title = ['GEOS-5 24h Observation Impact Time Series','<date_interval_with_time>','<short_domain_name>, <name>, <statistic>, <channel>']

document(
    plot = [
        timeseriesplot(
            { 'graphics.bar_width_factor': 1.0, 'title_font.size': 'medium', 'graphics.grid': True, 'graphics.edgewidth': 0.05, 'graphics.color': 'bk' },
            xaxis = axis(tick_label_size = 'small',title_size = 'small'),
            yaxis = axis(tick_label_size = 'small',title_size = 'small'),
            colorbar_title = '',
            has_legend = False,
            colormap = colormap(min = -0.4,max = 0.1,step = 0.05,tick_label_size='x-small',title_size='small'),
            curve = bar(plotdata = obsdata(datefile = 'dates.def')),
            title = title,
            plotdata = obsdata(statistic = 'impact_per_anl',level='all'),
            comment = commentexpver(display=['line','expver'],position='best_angled',style='--')
        ),
        timeseriesplot(
            { 'graphics.bar_width_factor': 1.0, 'title_font.size': 'medium', 'graphics.grid': True, 'graphics.edgewidth': 0.05, 'graphics.color': 'bk' },
            xaxis = axis(tick_label_size = 'small',title_size = 'small'),
            yaxis = axis(tick_label_size = 'small',title_size = 'small'),
            colorbar_title = '',
            has_legend = False,
            colormap = colormap(min = -1.e-5,max = -1.e-8,step = (-1.e-8 - -1.e-5) / 2,tick_label_size='x-small',title_size='small'),
            curve = bar(plotdata = obsdata(datefile = 'dates.def')),
            plotdata = obsdata(statistic = 'impact_per_ob',level='all'),
            title = title,
            comment = commentexpver(display=['line','expver','date'],position='best_angled',style='--')
        ),
        timeseriesplot(
            { 'graphics.bar_width_factor': 1.0, 'title_font.size': 'medium', 'graphics.grid': False, 'graphics.edgewidth': 0.05, 'graphics.color': 'bk' },
            xaxis = axis(tick_label_size = 'small',title_size = 'small'),
            yaxis = axis(tick_label_size = 'small',title_size = 'small', min = 48),
            colorbar_title = '',
            has_legend = False,
            colormap = colormap(min = 48.0,max = 54.0,step = 1.0,tick_label_size='x-small',title_size='small'),
            curve = bar(plotdata = obsdata(datefile = 'dates.def')),
            plotdata = obsdata(statistic = 'beneficial',level='all'),
            title = title,
            comment = [commentline(
                    position = 50,
                    style = '--',
                    linewidth = 0.8,
            ),
            commentexpver(display=['line','date'],position='best_angled',style='--')
            ]
        )
    ],
    plotdata = obsdata(
        date = Dates(begin,end,24),
        type = 'im',
        variable = 'xvec',
        domain = ['global'],
        database = database,
        kx = 220,
        kt = [4,5],
        name = 'radiosonde wind'
    ),
    datahook = printhook('name','domain_name','date','statistic','value',hidemissing=True),
    interactive = False,
    output = 'timeseries' + '<name>__<statistic>.png',
    size = [9,4.77]
)
