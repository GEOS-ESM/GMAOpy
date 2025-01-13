from semperpy.verify.scorefilereader import ScoreFileReader
from semperpy.verify.scorestepfilereader import ScoreStepFileReader

f = ScoreStepFileReader('data.txt')
result  = f(
    date = [2010070800,2010070812,2010070900,2010070912],
    step = [12,24,36,48,60,72],
    score = 'rmsfe',
    level = 500,
    parameter = 'h',
    domain = 'n.amer',
)

for key,items in list(result.items()):
    print(key,items)
