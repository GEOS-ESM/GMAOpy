rom MetPy import *
import numpy.ma as ma

fa=ma.array([23.,25.,27.,26.,29.])
va=ma.array([22.,23.,24.,21.,28.])
w=ma.array([0.71,0.72,0.73,0.74,0.75])

# Numpy version:
maf = ma.sum(fa*w)/ma.sum(w)
mav = ma.sum(va*w)/ma.sum(w)
corr = ma.sum((fa-maf)*(va-mav)*w)/ma.sum(w)
sdav = ma.sqrt(ma.sum((va-mav)**2*w)/ma.sum(w))
sdaf = ma.sqrt(ma.sum((fa-maf)**2*w)/ma.sum(w))
ccaf = corr / (sdav*sdaf)
print ccaf*100.,maf,sdaf,mav,sdav

fa=Matrix(fa.tolist())
va=Matrix(va.tolist())
w=Matrix(w.tolist())

# MetPy version:
s = Scores(fa,va,weights=w)
print s.correlation(),
s = Scores(fa,weights=w)
print s.mean(),s.stddev(),
s = Scores(va,weights=w)
print s.mean(),s.stddev()
##################################

To apply this to real data I would do:

##############unverified###############
from MetPy import *
import numpy
import numpy.ma as ma

f=FieldSet("field.grib")

# sorry, this is dirty################
fi=FieldIndex(f,'type','step','time')
fc = fi.access(type='fc')[0].matrix().export_to_Numpy()
an = fi.access(type='an',time=12)[0].matrix().export_to_Numpy()
cl = fi.access(type='em')[0].matrix().export_to_Numpy()
############################

coords = numpy.array([[x[1],(x[0]+360.)%360] for x in f[0].geoIterator()])
lats = coords[:,0]
lons = coords[:,1]

weights = numpy.cos(coords[:,0]*numpy.pi/180.)

domains = [ # [N W S E]
       [65.,355.,40.,25.],
       [20.,0.,-20.,360.],
]

class GeoDomain(object):
       def __init__(self,N,W,S,E):
               self.W_ = (W+360)%360
               self.E_ = (E+360)%360
               self.N_ = N
               self.S_ = S
               if (self.E_-self.W_)%360==0: # zonal band
                       self.condLon_ = lambda llon: True
               elif self.E_<self.W_: # the principal meridien in the domain
                       self.condLon_ = lambda llon:
ma.logical_or(llon>=self.W_,llon<=self.E_)
               else:
                       self.condLon_ = lambda llon:
ma.logical_and(llon>=self.W_,llon<=self.E_)
               self.condLat_ = lambda llat:
ma.logical_and(llat>=self.S_,llat<=self.N_)

       def insiders(self,llats,llons):
               return ma.logical_and(self.condLon_(llons),self.condLat_(llats))

fa = fc-cl
va = an-cl

for N,W,S,E in domains:
       g=GeoDomain(N,W,S,E)
       #mask outside points out:
       w = ma.array(weights,mask=ma.logical_not(g.insiders(lats,lons)))
       maf = ma.sum(fa*w)/ma.sum(w)
       mav = ma.sum(va*w)/ma.sum(w)
       corr = ma.sum((fa-maf)*(va-mav)*w)/ma.sum(w)
       sdav = ma.sqrt(ma.sum((va-mav)**2*w)/ma.sum(w))
       sdaf = ma.sqrt(ma.sum((fa-maf)**2*w)/ma.sum(w))
       ccaf = corr / (sdav*sdaf)
       print ccaf*100.,maf,sdaf,mav,sdav
###########################################
