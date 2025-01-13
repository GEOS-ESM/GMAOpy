from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.fields.netcdf.file import File
from semperpy.core.date import Date
from semperpy.core.index import Index

config = GMAOConfig(verbose=0)
r = File('verif.nc', config)
fs = r.all_fields()

mapping = dict (f='fc', a='an', c='cl'   )
index = Index('parameter', 'type', 'date', 'step', 'level')
min,max = r.getLimits('time')
for f in fs:
#    print f.metadata()
    p = f.get('parameter')
    f.set('parameter',p[0])
    f.set('type',mapping[p[1]])
    f.set('step',0)
    if not 'levels' in f:
       f.set('levels',0)
    f.set('level',f.get('levels'))
    if p[1] =='f':
       v = Date(f.get('date'))
       f.set('date',min.intvalue())
       f.set('step', v-min)
       
    index.insert(f,**f.metadata())
print(index)
