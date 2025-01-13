from Directives import *

c = Compute(
    variables = Variable(
        parameter = ["H","T"],
        level_type = "p",
        level = 850
    ),
    forecast = Forecast(
        date = 2010062200,
        step = [12,24,36],
        expid = "d520_fp",
        group = "met",
        type = "fc",
        field = "inst",
        dimension = "3d",
    ),
    reference = Analysis(
        expid = "d520_fp",
        group = "met",
        type = "asm",
        field = "inst",
        dimension = "3d",
    ),
)
c.checkLanguage()
print(c)
