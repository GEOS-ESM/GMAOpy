from semperpy.directives import *
from semperpy.plot.basemap import *
from semperpy.verify.forecast import forecast

p = retrieve(
    variables = [
        variable(
            parameter = 't',
            level = [300]
        ),
    ],
    fields = forecast(
        source = 'oper',
        date = [2010070900],
        step = [24,48],
        expver = 'd520',
    ),
)
print(p)
fieldset = list(p.values())
print(fieldset)
