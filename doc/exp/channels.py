import sys
from gmaopy.modules.obsplot import *

expver = 'd572_sw'
dates = Dates(2010080100,2010090100,24)
database = 'im_exp'
filename = 'channels.def'
minimum = 1.0e+3
maximum = 1.0e+4

title = ['GEOS-5 24h Observation Impact Per Channel','<date_interval_with_time>','<short_domain_name>, <name>, <statistic>','db=<database> expid=<expver>']

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
            curve = bar(),
            colormap = colormap(min = minimum,max = maximum,scale = 'log',tick_label_size='x-small',title_size='small'),
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
            curve = bar(),
            colormap = colormap(min = minimum,max = maximum,scale = 'log',tick_label_size='x-small',title_size='small'),
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
            curve = bar(),
            colormap = colormap(min = minimum,max = maximum,scale = 'log',tick_label_size='x-small',title_size='small'),
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
            curve = bar(),
            colormap = colormap(min = minimum,max = maximum,scale = 'log',tick_label_size='x-small',title_size='small'),
        ),
    ],
    plotdata = obsdata(
        filename = filename,
        date = dates,
        type = 'im',
        variable = 'xvec',
        domain = ['global','n.hem','s.hem','tropics'],
        database = database,
        channel = 'all',
        expver = expver,
    ),
    interactive = False,
    output = 'channels_all+<name>+<domain_name>+<statistic>.png', 
    size = [6.75,4.77]
)
