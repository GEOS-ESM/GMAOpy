from semperpy.directives import *
from semperpy.plot.matplotlib import *
from semperpy.verify.analysis import analysis

p = geoplot(
    contour = GeoContourFill(colorbar=ColorBar(aspect=15)),
    layout = [1,1],
    fields = retrieve(
        fields = analysis(
            source = 'odas',
            expver = 'mvoi_1992_nosla',
            date = [1993030403],
        ),
        variables = variable(
            parameter = 't',
            level = [300],
        ),
        trydap = False,
        returned = "fieldset"
    ),
)
