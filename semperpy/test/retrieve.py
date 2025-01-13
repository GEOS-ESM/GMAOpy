from semperpy.directives import *
from semperpy.verify.analysis import analysis

p = retrieve(
    variables = [
        variable(
            parameter = 't',
            lat = [-30,30],
            lon = [165],
            level = [0,500],
        ),
    ],
    fields = analysis(
        source = 'odas',
        expver = 'mvoi_1992_nosla',
        date = [1993030403],
    ),
    trydap = False,
    returned = "array"
)
print(p)
a = list(p.values())
print(a[0][0].shape)
