
time = {
    'month': 30,
    'three_month': 90,
    'year' : 364,
}

scripts = dict(
    timeseries = dict(
        all = ('timeseries_all.def','timeseries_all'),
        rad = ('timeseries_radiances.def','timeseries_radiances')
    ),
    summary = dict(
        all = ('summary_all.def','summary_all',1.0e+3,1.0e+6),
        rad = ('summary_radiances.def','summary_radiances',1.0e+4,1.0e+6)
    ),
    channels = dict(
        all = ('channels_all.def','channels_all',1.0e+3,1.0e+4),
    ),
)

def timeInterval(interval_name):
    return time[interval_name] * 24

def settings(script,option):
    return scripts[script][option]
