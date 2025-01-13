import sys
from gmaopy.modules.obsplot import *
import settings

date            = Date(sys.argv[1])
expver          = sys.argv[2]
interval_name   = sys.argv[3]
database        = sys.argv[4]
option          = sys.argv[5]

interval = settings.timeInterval(interval_name)
filename,prefix = settings.settings('timeseries',option)
begin = date - interval

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
            plotdata = obsdata(statistic = 'impact_per_anl'),
        ),
        timeseriesplot(
            { 'graphics.bar_width_factor': 1.0, 'title_font.size': 'medium', 'graphics.grid': True, 'graphics.edgewidth': 0.05, 'graphics.color': 'bk' },
            xaxis = axis(tick_label_size = 'small',title_size = 'small'),
            yaxis = axis(tick_label_size = 'small',title_size = 'small'),
            colorbar_title = '',
            has_legend = False,
            colormap = colormap(min = -1.e-5,max = -1.e-8,step = (-1.e-8 - -1.e-5) / 2,tick_label_size='x-small',title_size='small'),
            curve = bar(plotdata = obsdata(datefile = 'dates.def')),
            plotdata = obsdata(statistic = 'impact_per_ob'),
            title = title,
        ),
        timeseriesplot(
            { 'graphics.bar_width_factor': 1.0, 'title_font.size': 'medium', 'graphics.grid': False, 'graphics.edgewidth': 0.05, 'graphics.color': 'bk' },
            xaxis = axis(tick_label_size = 'small',title_size = 'small'),
            yaxis = axis(tick_label_size = 'small',title_size = 'small', min = 48),
            colorbar_title = '',
            has_legend = False,
            colormap = colormap(min = 48.0,max = 54.0,step = 1.0,tick_label_size='x-small',title_size='small'),
            curve = bar(plotdata = obsdata(datefile = 'dates.def')),
            plotdata = obsdata(statistic = 'beneficial'),
            title = title,
            comment = commentline(
                    position = 50,
                    style = '--',
                    linewidth = 0.8,
            )
        ),
        timeseriesplot(
            { 'graphics.bar_width_factor': 1.0, 'title_font.size': 'medium', 'graphics.grid': True, 'graphics.edgewidth': 0.05, 'graphics.color': 'bk' },
            xaxis = axis(tick_label_size = 'small',title_size = 'small'),
            yaxis = axis(tick_label_size = 'small',title_size = 'small'),
            colorbar_title = '',
            has_legend = False,
            colormap = colormap(min = 1.0e+3,max = 1.0e+6,scale='log',tick_label_size='x-small',title_size='small'),
            curve = bar(plotdata = obsdata(datefile = 'dates.def')),
            plotdata = obsdata(statistic = 'count_per_anl'),
            title = ['GEOS-5 24h Observation Impact Time Series','<date_interval_with_time>','<short_domain_name>, <name>, Observation Count'],
        )
    ],
    plotdata = obsdata(
        filename = filename,
        date = Dates(begin.intvalue(),date.intvalue(),24),
        type = 'im',
        variable = 'xvec',
        domain = ['global','n.hem','s.hem','tropics'],
        database = database,
    ),
    interactive = False,
    output = prefix + '+%s+<name>+<domain_name>+<statistic>.png' % interval_name,
    size = [9,4.77]
)
