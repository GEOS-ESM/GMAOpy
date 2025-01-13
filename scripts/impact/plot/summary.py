import sys
from gmaopy.modules.obsplot import *
import settings

date            = Date(sys.argv[1])
expver          = sys.argv[2]
interval_name   = sys.argv[3]
database        = sys.argv[4]
option          = sys.argv[5]

interval = settings.timeInterval(interval_name)
filename,prefix,min,max = settings.settings('summary',option)
begin = date - interval

title = ['GEOS-5 24h Observation Impact Summary','<date_interval_with_time>','<short_domain_name>, <statistic>']
document(
    plot = [
        summaryplot(
            { 'graphics.bar_width_factor': 1.0, 'graphics.grid': False, 'title_font.size': 'medium' },
            xaxis = axis(tick_label_size = 'small',title_size = 'small'),
            yaxis = axis(tick_label_size = 'small',title_size = 'small'),
            plotdata = obsdata(
                filename = filename,
                statistic = 'impact_per_anl',
                colormap_statistic = 'count_per_anl',
            ),
            curve = bar(plotdata = obsdata(datefile = 'dates.def')),
            title = title,
            colormap = colormap(min = min,max = max,scale = 'log',tick_label_size='x-small',title_size='small')
        ),
        summaryplot(
            { 'graphics.bar_width_factor': 1.0, 'graphics.grid': False, 'title_font.size': 'medium' },
            xaxis = axis(tick_label_size = 'small',title_size = 'small'),
            yaxis = axis(tick_label_size = 'small',title_size = 'small'),
            plotdata = obsdata(
                filename = filename,
                statistic = 'impact_per_ob',
                colormap_statistic = 'count_per_anl',
            ),
            curve = bar(plotdata = obsdata(datefile = 'dates.def')),
            title = title,
            colormap = colormap(min = min,max = max,scale = 'log',tick_label_size='x-small',title_size='small')
        ),
        summaryplot(
            { 'graphics.bar_width_factor': 1.0, 'graphics.grid': False, 'title_font.size': 'medium' },
            xaxis = axis(tick_label_size = 'small',title_size = 'small',min = 48),
            yaxis = axis(tick_label_size = 'small',title_size = 'small'),
            plotdata = obsdata(
                filename = filename,
                statistic = 'beneficial',
                colormap_statistic = 'count_per_anl',
            ),
            curve = bar(plotdata = obsdata(datefile = 'dates.def')),
            title = title,
            sort = 'increasing',
            colormap = colormap(min = min,max = max,scale = 'log',tick_label_size='x-small',title_size='small'),
            comment = commentline(
                    position = 50,
                    style = '--',
                    linewidth = 0.8,
            ),
            xtitle = '<statistic> <unit>',
        ),
    ],
    plotdata = obsdata(
        date = Dates(begin.intvalue(),date.intvalue(),24),
        type = 'im',
        variable = 'xvec',
        domain = ['global','n.hem','s.hem','tropics'],
        database = database,
    ),
    interactive = False,
    output = prefix + '+%s+<domain_name>+<statistic>.png' % interval_name,
    size = [6.75,4.77]
)
