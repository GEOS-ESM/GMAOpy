#!/usr/bin/env python
#
# Simple script testing the ext()/expr() methods
#

from types import *
from pylab import *
from grads import GrADS
from pylab import prctile

def print_stats(name,x=None):
    "Prints simple stats"
    if type(name) is not StringType:
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


if __name__ == "__main__":

#   Start GrADS and open the data file
#   ----------------------------------
    ga = GrADS(Echo=False,Window=False) # quiet as a mouse
    fh = ga.open('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM')
    print(fh)

    print_stats('__header__','Slicing Examples with PyGrADS')

#   XY slices
#   ---------
    ga('set time 0Z5feb2003 21Z5feb2003') # 1 day worth of data
    ga('set lon -179.375 179.375')
    ga('set lat -90 90')
    slp = ga.expr('slp')  # by default global lat/lon domain
    print(slp.shape)
    print_stats('SLP XY',slp/100.-1000.) # notice scaling

#   XYT slices with lat/lon subsetting
#   ----------------------------------
    ga('set lon -140 -40') # restrict longitude to [140W,40W]
    ga('set lat 20 50')    # restrict latitude  to [20N,50N] 
    ga('set time 0Z5feb2003 21Z5feb2003') # 1 day worth of data
    slp = ga.expr('slp')
    print(slp.shape)
    print_stats('SLP XYT',slp/100.-1000.)

#   XYZ slices
#   ----------
    ga('set time 12Z13nov2003')  # Jonas' birthday
    ga('set lev 300 200')        # range of levels
    speed = ga.expr('mag(u,v)')  # mag() is grads function for wind speed
    print(speed.shape)
    print_stats('SPEED XYZ',speed)


#   XZT slices
#   ----------
    ga('set t 2 4') # you can also use "x,y,z,t" for accessing data in index space
    ga('set y 20')
    ga('set z 3 5')
    u = ga.expr('u')
    print_stats('U XZT',u)

    print_stats('__footer__')

    

