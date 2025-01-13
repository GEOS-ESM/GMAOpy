import sys
from gmaopy.modules.obsplot import *
import settings

date            = Date(sys.argv[1])
expver          = sys.argv[2]
interval_name   = sys.argv[3]
database        = sys.argv[4]
option          = sys.argv[5]

interval = settings.timeInterval(interval_name)
filename,prefix,min,max = settings.settings('channels',option)
begin = date - interval

title = ['GEOS-5 24h Observation Impact Per Channel','<date_interval_with_time>','<short_domain_name>, <name>, <statistic>']

document(
    plot = [
        channelplot(
            { 'graphics.grid': False, 'graphics.bar_width_factor': 1.0, 'title_font.size': 'medium',  'graphics.edgewidth': 0.05 },
            xaxis = axis(tick_label_size = 'small',title_size = 'small'),
            yaxis = axis(tick_label_size = 'small',title_size = 'small',absolute_max = 12),
            title = title,
            plotdata = obsdata(
                statistic = 'impact_per_anl',
                colormap_statistic = 'count_per_anl',
            ),
            curve = bar(plotdata = obsdata(datefile = 'dates.def')),
            colormap = colormap(min = min,max = max,scale = 'log',tick_label_size='x-small',title_size='small'),
            comment = commentline(
                    position = 0,
                    style = '-',
                    linewidth = 0.6,
            )
        ),
        channelplot(
            { 'graphics.grid': False, 'graphics.bar_width_factor': 1.0, 'title_font.size': 'medium',  'graphics.edgewidth': 0.05 },
            xaxis = axis(tick_label_size = 'small',title_size = 'small'),
            yaxis = axis(tick_label_size = 'small',title_size = 'small',absolute_max = 12),
            title = title,
            plotdata = obsdata(
                statistic = 'impact_per_ob',
                colormap_statistic = 'count_per_anl',
            ),
            curve = bar(plotdata = obsdata(datefile = 'dates.def')),
            colormap = colormap(min = min,max = max,scale = 'log',tick_label_size='x-small',title_size='small'),
            comment = commentline(
                    position = 0,
                    style = '-',
                    linewidth = 0.6,
            )
        ),
        channelplot(
            { 'graphics.grid': False, 'graphics.bar_width_factor': 1.0, 'title_font.size': 'medium',  'graphics.edgewidth': 0.05 },
            xaxis = axis(tick_label_size = 'small',title_size = 'small',min = 48),
            yaxis = axis(tick_label_size = 'small',title_size = 'small',absolute_max = 12),
            title = title,
            plotdata = obsdata(
                statistic = 'beneficial',
                colormap_statistic = 'count_per_anl',
            ),
            curve = bar(plotdata = obsdata(datefile = 'dates.def')),
            colormap = colormap(min = min,max = max,scale = 'log',tick_label_size='x-small',title_size='small'),
            comment = commentline(
                    position = 50,
                    style = '--',
                    linewidth = 0.8,
            )
        ),
        channelplot(
            { 'graphics.grid': False, 'graphics.bar_width_factor': 1.0, 'title_font.size': 'medium',  'graphics.edgewidth': 0.05 },
            xaxis = axis(tick_label_size = 'small',title_size = 'small'),
            yaxis = axis(tick_label_size = 'small',title_size = 'small',absolute_max = 12),
            title = ['GEOS-5 24h Observation Impact Per Channel','<date_interval_with_time>','<short_domain_name>, <name>, Observation Count'],
            plotdata = obsdata(
                statistic = 'count_per_anl',
                colormap_statistic = 'count_per_anl',
            ),
            curve = bar(plotdata = obsdata(datefile = 'dates.def')),
            colormap = colormap(min = min,max = max,scale = 'log',tick_label_size='x-small',title_size='small'),
        ),
    ],
    plotdata = obsdata(
        filename = 'channels.def',
        date = Dates(begin.intvalue(),date.intvalue(),24),
        type = 'im',
        variable = 'xvec',
        domain = ['global','n.hem','s.hem','tropics'],
        database = database,
        channel = 'all',
    ),
    interactive = False,
    output = prefix + '+%s+<name>+<domain_name>+<statistic>.png' % interval_name,
    size = [6.75,4.77]
)
