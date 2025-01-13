import copy
import bisect
from collections import defaultdict
import numpy.ma as ma
from semperpy.core.tools import to_list, nestedLoops
from semperpy.core.configfile import ConfigFile
from semperpy.core.index import Index
from semperpy.slicing.arraygenerator import ArrayGenerator
from semperpy.plot.plotdata import PlotData
from semperpy.plot.dimension import Dimension
from gmaopy.storage.reader import Reader
from gmaopy.stats.statistics import Statistics

class StatData(PlotData):

    def __init__(self,*args,**kwargs):
        self.value_ = None
        self.colormap_value_ = None
        super(StatData,self).__init__(*args,**kwargs)

    #------------------------------------------------------------------
    # properties
    #------------------------------------------------------------------
    def get_value(self):
        return self.value_
    def set_value(self,new):
        self.value_ = new
    value = property(get_value,set_value)

    def get_colormapvalue(self):
        if self.colormap_value_ is not None:
            return self.colormap_value_
        return self.value_
    def set_colormapvalue(self,new):
        self.colormap_value_ = new
    colormapvalue = property(get_colormapvalue,set_colormapvalue)
    #------------------------------------------------------------------
    
    def cmp(x,y):
        if x < y:
            return -1
        elif x > y:
            return 1
        else:
            return 0

    def data_columns(self,columns):
        data_columns = {}
        for index in range(len(columns)):
            data_columns[columns[index]] = index 
        return data_columns

    def datesAndExpvers(self,filename,dates):
        if hasattr(self,'allexpvers_'):
            return self.alldates_, self.allexpvers_
        # this is rather ugly, but I don't want to assume that dates in the 
        # directive have a constant step or don't have gaps. I can't think of anything better.
        dd = set(dates) # bad because dates is now 2d
        specs = ConfigFile(filename)
        specs = [ specs[x] for x in specs ]
        # sort sections by starting dates
#        specs.sort(lambda a,b: cmp(int(a['start']),int(b['start'])))
        specs = sorted(specs,key= lambda a: a['start'])
        # convert to integer
        for spec in specs:
            spec['start'] = int(spec['start'])
            spec['end'] = int(spec['end'])
        start = dates[0]
        end = dates[-1]
        # first check if we have info to proceed
        if start < specs[0]['start']:
            raise ValueError('The dates specified start before (%d) the first date in the datefile (%d)' % (start,specs[0]['start']))
        if end > specs[-1]['end']:
            raise ValueError('The dates specified end after (%d) the last date in the datefile (%d)' % (end,specs[0]['start']))
        startspec = 0
        endspec = len(specs) - 1
        for i in range(len(specs)):
            spec = specs[i]
            if start >= spec['start'] and start <= spec['end']:
                startspec = i
            if end >= spec['start'] and end <= spec['end']:
                endspec = i
        expvers = []
        alldates = []
        for i in range(startspec,endspec+1):
            a = bisect.bisect_left(dates,specs[i]['start'])
            b = bisect.bisect_right(dates,specs[i]['end'])
            if a != b:
                alldates.append(dates[a:b])
                expvers.append(specs[i]['expver'])
        self.alldates_ = alldates
        self.allexpvers_ = expvers
        return alldates,expvers
            

    def better(self,statistic):
        return Statistics.create(self.category(),statistic).moreIsBetter()
    
    def moreIsBetter(self):
        return self.better(self['statistic'])

    def colorMapMoreIsBetter(self):
        return self.better(self['colormap_statistic'])

    def __copy__(self):
        new = super(StatData,self).__copy__()
        new.value_ = self.value_
        new.colormap_value_ = self.colormap_value_
        if 'observer' in self:
            new['observer'] = [ copy.copy(x) for x in self['observer'] ]
        return new

    def doRetrieve(self,owner,what):
        axis_name = self.draw_index_columns(what)
        """
        We call the prepare_values method on the dimension we plot against
        (e.g. level, date) to have a chance to sort the values in the order
        we want for a particular plot.
        """
        if not 'expver' in self and not 'datefile' in self:
            print('At least "expver" of "datefile" should be specified, not specifying any experiment ID could lead to misleading information.')
        for name in axis_name:
            index_dimension = Dimension.createDimensionFilter(name,what)
            self[name] = index_dimension.prepare_values(self,self[name])
        index_columns = self.index_columns(what)
        actor = Statistics.create(self.category(),self['statistic'])
        columns = self.columns(what) + actor.columns()
        data_columns = self.data_columns(columns)
        self.value_ = self.retrieve(owner,index_columns,columns,data_columns,self['statistic'],actor)
        if 'colormap_statistic' in self:
            actor = Statistics.create(self.category(),self['colormap_statistic'])
            self.colormap_value_ = self.retrieve(owner,index_columns,columns,data_columns,self['colormap_statistic'],actor)
        else:
            self['colormap_statistic'] = self['statistic']

    def retrieve(self,owner,index_columns,columns,data_columns,statistic,actor):
        reader = Reader.create(self['storage'],self['database'])
        if 'datefile' in self:
            alldates,allexpvers = self.datesAndExpvers(self['datefile'],self['date'])
            self['date'] = []
        other = copy.copy(self)
        statistic = actor.requirements_db()
        other['statistic'] = statistic

        data = []
        if 'datefile' in self:
            for date,expver in zip(alldates,allexpvers):
                other['date'] = date
                self['date'] += date
                other['expver'] = expver
                data += reader(other,columns)
        else:
            data = reader(other,columns)
        keys = index_columns
        retrieved = []
        if len(keys) == 0:
            retrieved = actor.compute_db(data_columns,data,self['variable'])
        else:
            gen = ArrayGenerator(missing_value = Statistics.missing_value)
            index = Index(*keys)
            for d in data:
                params = {}
                for key in keys:
                    params[key] = d[data_columns[key]]
                index.insert(d,**params)
            combinations = {}
            shape = 1
            multi_shape = []
            for key in keys:
                ll = len(to_list(self[key]))
                shape *= ll
                multi_shape.append(ll)
                combinations[key] = self[key]
            result = gen.create((shape))
            all = nestedLoops(combinations,keys)
            i = 0
            for v in all:
                final = index.access(**v)
                current = actor.compute_db(data_columns,final,self['variable'])
                assert(len(current) == 1)
                result[i] = current[0]
                i += 1
            retrieved = gen.postProcess(result)
            if len(multi_shape) > 1:
                retrieved = ma.reshape(retrieved,multi_shape)
            if 'transform' in self:
                for t in self['transform']:
                    retrieved = t(self,retrieved)
        return retrieved
