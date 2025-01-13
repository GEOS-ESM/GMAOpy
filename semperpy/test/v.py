import types
from pylab import *
from pylab import prctile

from gmaopy.netcdf.fieldreader import FieldReader


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

class Visitor(object):

    def __call__(self,slices,metadata):
        print(where,metadata)

print_stats('__header__','Slicing Examples with SemperPy')
f = FieldReader('file.hdf')
directive = dict(
    level = [1000,500],
    latitude = {-40:50},
    longitude = {-20:200},
    date = 2010070812,
    parameter = 'u',
)
v = f.readArray(directive,a = 2,b = 3)
print(v)
print(v.shape)
print_stats('',v)


print_stats('__footer__')
