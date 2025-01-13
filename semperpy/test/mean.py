import numpy as np
import matplotlib.pyplot as plt
from semperpy.verify.scorefilereader import ScoreFileReader
from semperpy.verify.scorestepfilereader import ScoreStepFileReader

steps = [12,24,36,48,60,72]
f = ScoreStepFileReader('data.txt')
rmsfe  = f(
    date = [2010070800,2010070812,2010070900,2010070912],
    step = steps,
    score = 'rmsfe',
    level = 500,
    parameter = 'h',
    domain = 'n.amer',
)
meanfe  = f(
    date = [2010070800,2010070812,2010070900,2010070912],
    step = steps,
    score = 'meanfe',
    level = 500,
    parameter = 'h',
    domain = 'n.amer',
)

mean_rms = np.zeros((len(steps)),np.float64)
for key,items in list(rmsfe.items()):
    mean_rms += items
mean_rms /= len(rmsfe)
mean_mean = np.zeros((len(steps)),np.float64)
for key,items in list(meanfe.items()):
    mean_mean += items
mean_mean /= len(meanfe)
figure = plt.figure()
curves = figure.add_subplot(111)
plt.xlabel('Time Step (h)')
plt.ylabel('Root mean square error (m)')
plt.axis([steps[0],steps[-1],min(mean_rms[0],mean_mean[0]),max(mean_rms[-1],mean_mean[-1])])
plt.xticks(steps)
curves.plot(steps,mean_rms)
curves.plot(steps,mean_mean)
plt.show()
