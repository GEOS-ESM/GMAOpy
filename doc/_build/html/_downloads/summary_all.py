import sys
from gmaopy.modules.obsplot import *

expver = 'd572_sw'
dates = Dates(2010080100,2010090100,24)
database = 'im_exp'
filename = 'summary_all.def'
minimum = 1.0e+3
maximum = 1.0e+6

title = ['GEOS-5 24h Observation Impact Summary','<date_interval_with_time>','<short_domain_name>, <statistic>', 'db=<database> expid=<expver>']
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
            curve = bar(),
            title = title,
            colormap = colormap(min = minimum,max = maximum,scale = 'log',tick_label_size='x-small',title_size='small'),
            xtitle = '<statistic> <unit>',
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
            curve = bar(),
            title = title,
            colormap = colormap(min = minimum,max = maximum,scale = 'log',tick_label_size='x-small',title_size='small'),
            xtitle = '<statistic> <unit>',
        ),
        summaryplot(
            { 'graphics.bar_width_factor': 1.0, 'graphics.grid': False, 'title_font.size': 'medium' },
            xaxis = axis(tick_label_size = 'small',title_size = 'small',minimum = 48),
            yaxis = axis(tick_label_size = 'small',title_size = 'small'),
            sort = 'decreasing',
            plotdata = obsdata(
                filename = filename,
                statistic = 'beneficial',
                colormap_statistic = 'count_per_anl',
            ),
            curve = bar(),
            title = title,
            colormap = colormap(min = minimum,max = maximum,scale = 'log',tick_label_size='x-small',title_size='small'),
            comment = commentline(
                    position = 50,
                    style = '--',
                    linewidth = 0.8,
            ),
            xtitle = '<statistic> <unit>',
            has_xtitle = True,
        ),
        summaryplot(
            { 'graphics.bar_width_factor': 1.0, 'graphics.grid': False, 'title_font.size': 'medium' },
            xtitle = 'Observation Count Per Analysis',
        xaxis = axis(tick_label_size = 'small',title_size = 'small'),
            yaxis = axis(tick_label_size = 'small',title_size = 'small',absolute_max = 12),
            sort = 'decreasing',
            plotdata = obsdata(
                filename = filename,
                statistic = 'count_per_anl',
                colormap_statistic = 'count_per_anl',
            ),
            curve = bar(),
            title = ['GEOS-5 24h Observation Impact Summary','<date_interval_with_time>','<short_domain_name>, Observation Count'],
            colormap = colormap(min = minimum,max = maximum,scale = 'log',tick_label_size='x-small',title_size='small'),
        ),
    ],
    plotdata = obsdata(
        date = dates,
        type = 'im',
        variable = 'xvec',
        domain = ['global','n.hem','s.hem','tropics'],
        database = database,
        expver = expver,
    ),
    interactive = False,
    output = 'summary_all+<domain_name>+<statistic>.png',
    size = [6.75,4.77]
)
