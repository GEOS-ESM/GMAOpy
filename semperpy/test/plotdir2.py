from semperpy.directives import *
from semperpy.plot.basemap import *
from semperpy.verify.forecast import forecast
from semperpy.verify.analysis import analysis

p = plot(
    contour = ContourFill(),
    geography = Geography(
                      projection='stereo',
                      hemisphere='north',
                      lon_0=270,
    ),
    fields = retrieve(
        fields = analysis(
            source = 'merra',
            date = [2010041500,2010041506],
        ),
        variables = variable(
            parameter = ['h','t'],
            level = [500],
        ),
    )
)
print(p)
