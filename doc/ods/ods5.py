import numpy as np
from gmaopy.ods.ods import ODS

reader = ODS('e561_tst_02.diag_conv.20110201_00z.ods')
levels = [5,7,10,20,30,50,70,100,150,200,250,300,400,500,700,850,925,1000]
mean_counts = np.zeros(len(levels),dtype = np.float64)

filter = reader.compile('((kt == 4) | (kt == 5)) & (kx == 220) & (qcexcl == 0)')
obs_levels = reader.sampleLevels(bins=levels)
obs = reader.read('obs')
for i in range(len(levels)):
    array = obs(filter & (obs_levels == levels[i]))
    mean_counts[i] += array.shape[0]

for i in range(len(levels)):
    print(mean_counts[len(levels) - i - 1])
