from semperpy.language.validate import validateChoice
from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.fields.netcdf.file import File
import types
from pylab import *
from pylab import prctile


def print_stats(name,x=None):
    "Prints simple stats"
    if type(name) is not bytes:
        x = name
        name = 'mean,stdv,rms,min,25%,median,75%,max: '
    if name == '__header__':
        print('')
        n = (80 - len(x))/2
        print(n * ' ' + x)
        print(n * ' ' + len(x) * '-')
        print('')
        print('   Name       mean      stdv      rms      min     25%    median     75%      max')
        print(' ---------  -------  -------  -------  -------  -------  -------  -------  -------')
    elif name == '__sep__':
        print(' ---------  -------  -------  -------  -------  -------  -------  -------  -------')
    elif name == '__footer__':
        print(' ---------  -------  -------  -------  -------  -------  -------  -------  -------')
        print('')
    else:
        xx = x.compressed() # remove UNDEFS
        ave = xx.mean()
        std = xx.std()
        rms = sqrt(ave*ave+std*std)
        prc = prctile(xx)
        print('%10s  %7.2f  %7.2f  %7.2f  %7.2f  %7.2f  %7.2f  %7.2f  %7.2f  '%\
            (name,ave,std,rms,prc[0],prc[1],prc[2],prc[3],prc[4]))

print_stats('__header__','Slicing Examples with SemperPy')

r = File('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM',GMAOConfig(ignore_missing=True,verbose=0))
directive = dict(
    parameter = 'SLP',
    date = [2003020500,2003020521],
)
slp,fieldset = r.slice(directive)
slp = slp / 100.0 - 1000.0
print(slp.shape)
print_stats('SLP XY',slp)

directive = dict(
    parameter = 'slp',
    date = [2003020500,2003020521],
    lonitude = [-140,-40],
    latitude = [20,50]
)
slp,fieldset = r.slice(directive)
slp = slp / 100.0 - 1000.0
print(slp.shape)
print_stats('SLP XY',slp)

directive = dict(
    parameter = 'u',
    level = [300,200],
    date = [2003111312],
    longitude = [-140,-40],
    latitude = [20,50]
)

u,fieldset = r.slice(directive)
directive['parameter'] = 'v'
v,fieldset = r.slice(directive)
speed = sqrt((u * u) + (v * v))
print(speed.shape)
print_stats('SPEED XYZ',speed)

print_stats('__footer__')
