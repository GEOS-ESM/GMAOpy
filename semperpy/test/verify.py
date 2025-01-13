from semperpy.directives import *
from semperpy.verify import *

c = compute(
    fc = forecast(
        date = [2010070800,2010070812,2010070900,2010070912],
        step = [12,24,36,48,60,72],
        expid = 'd520',
    ),
    todolist = todolist(
        parameter = 'h',
        level = [1000,500],
        score = ['meanfe','rmsfe'],
        domain = ['n.amer','europe','n.atl','n.pac']
    )
)

print(c)
