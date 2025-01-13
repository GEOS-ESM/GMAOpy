import sys
from gmaopy.modules.obsplot import *

expver = 'd572_sw'
dates = Dates(2010080100,2010090100,24)
database = 'im_exp'
filename = 'timeseries_all.def'

title = ['GEOS-5 24h Observation Impact Time Series','<date_interval_with_time>','<short_domain_name>, <name>, <statistic>, <channel>','db=<database> expid=<expver>']

document(
    plot = [
        timeseriesplot(
            { 'graphics.bar_width_factor': 1.0, 'title_font.size': 'medium', 'graphics.grid': True, 'graphics.edgewidth': 0.05, 'graphics.color': 'bk' },
            xaxis = axis(tick_label_size = 'small',title_size = 'small'),
            yaxis = axis(tick_label_size = 'small',title_size = 'small'),
            colorbar_title = '',
            has_legend = False,
            colormap = colormap(min = -0.4,max = 0.1,step = 0.05,tick_label_size='x-small',title_size='small'),
            curve = bar(),
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
            curve = bar(),
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
            curve = bar(),
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
            curve = bar(),
            plotdata = obsdata(statistic = 'count_per_anl'),
            title = ['GEOS-5 24h Observation Impact Time Series','<date_interval_with_time>','<short_domain_name>, <name>, Observation Count'],
        )
    ],
    plotdata = obsdata(
        filename = filename,
        date = dates,
        type = 'im',
        variable = 'xvec',
        domain = ['global','n.hem','s.hem','tropics'],
        database = database,
        expver = expver
    ),
    interactive = False,
    output = 'timeseries_all+<name>+<domain_name>+<statistic>.png',
    size = [9,4.77]
)
