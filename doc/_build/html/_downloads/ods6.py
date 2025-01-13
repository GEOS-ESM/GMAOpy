import math
import numpy as np
import numpy.ma as ma
from semperpy.core.date import Date, Dates
from semperpy.core.tools import substitute_unix_dates
from semperpy.observations.observation import Observation
from gmaopy.ods.ods import ODS

# date formats documented in "man strftime"
filename = 'e561_tst_02.diag_conv.date(%Y%m%d_%H)z.ods'
levels = [5,7,10,20,30,50,70,100,150,200,250,300,400,500,700,850,925,1000]
mean_counts = np.zeros(len(levels),dtype = np.float64)
rms_oma = np.zeros(len(levels),dtype = np.float64)
mean_oma = np.zeros(len(levels),dtype = np.float64)

for date in Dates(2011020100,2011022818,6):
    file = substitute_unix_dates(filename,'date',Date(date))
    print(file)
    reader = ODS(file)
    filter = reader.compile('((kt == 4) | (kt == 5)) & (kx == 220)')
    obs_levels = reader.sampleLevels(bins=levels)
    oma = reader.read('oma')
    for i in range(len(levels)):
        array = oma(filter & obs_levels == levels[i])
        result = array.compressed()
        mean_counts[i] += result.shape[0]
        mean_oma[i] += np.sum(result)
        result *= result
        rms_oma[i] += np.sum(result)

for i in range(len(levels)):
    rms_oma[i] /= mean_counts[i]
    rms_oma[i] = np.sqrt(rms_oma[i])
    mean_oma[i] /= mean_counts[i]
