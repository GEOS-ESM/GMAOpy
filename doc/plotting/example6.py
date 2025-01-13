from gmaopy.modules.obsplot import *

document(
    plotdata = obsdata(
        type = 'im',
        database = 'im_ops',
        variable = 'xvec',
        domain = ['global','n.hem'], 
        expver = 'e562p5_fp',
        level = [1000,500],          
        statistic = 'impact_per_anl',
        date = Dates(2011030100,2011033100,24),
    ),
    plot = timeseriesplot(
        {
            'graphics.bar_color' : 'khaki',
            'yaxis.max_bound_padding' : 0.15          #<- give some space
        },
        title = [None,None,'<statistic>','<parameter>'],  #<- modify title template
        curve = bar(
            plotdata = obsdata(
                kx = [120,220,221,132,229,232],
                kt = [4,5,11,44],
            ),
            legend = '<domain_name> <level>',         #<- modify legend template
        ),
        has_ytitle = False       
    ),
    layout = [2,2],             
    has_title = True,             
    interactive = False,
    output = 'example6.png',
)
