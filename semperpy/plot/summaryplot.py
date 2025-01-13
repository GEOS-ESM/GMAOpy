from collections import OrderedDict
from gmaopy.stats.statistics import Statistics
from semperpy.plot.colorbarplot import ColorbarPlot
import functools

def cmp(x,y):
    if x < y:
        return -1
    elif x > y:
        return 1
    else:
        return 0

def sortIncreasing(a,b):
    aval = max([ x.data.value[0] for x in a ])
    bval = max([ x.data.value[0] for x in b ])
    return cmp(bval,aval)

def sortDecreasing(a,b):
    aval = max([ x.data.value[0] for x in a ])
    bval = max([ x.data.value[0] for x in b ])
    return cmp(aval,bval)

def sortRankIncreasing(a,b):
    aval = min([ int(x.data.get('rank',100000)) for x in a ])
    bval = min([ int(x.data.get('rank',100000)) for x in b ])
    return cmp(bval,aval)

def sortRankDecreasing(a,b):
    aval = max([ int(x.data.get('rank',-1)) for x in a ])
    bval = max([ int(x.data.get('rank',-1)) for x in b ])
    return cmp(aval,bval)

class SummaryPlot(ColorbarPlot):

    sort_ = dict(
        decreasing = sortDecreasing,
        increasing = sortIncreasing,
        rank_decreasing = sortRankDecreasing,
        rank_increasing = sortRankIncreasing,
    )
    
    def sortCurves(self,curves):
        sort = self['sort']
        vals = self.gatherCurves(curves)
        if sort is not None:
            if not sort in self.sort_:
                raise IndexValue('%s is unknown for sorting curves')
            all = []
            for curves in vals.values():
                all.append(curves)
#            print(all[0]) 
#            all.sort(self.sort_[sort])
            all = sorted(all,key=functools.cmp_to_key(self.sort_[sort]))
            curves = []
            for a in all:
                curves += a
        else:
            curves = []
            for a in vals.values():
                curves += a
        return curves

    def eliminateMissing(self,curves):
        if self['removeMissing']:
            curves = [ x for x in curves if x.data.value[0] != Statistics.missing_value ]
        return curves

    def draw(self,layout,subplot):
        vals = self.gatherCurves(self.curves_)
        count = 0
        all = []
        for curves in vals.values():
            for c in curves:
                c.group_ = count
            all += curves
            count += 1
        self.curves_ = all
        super(SummaryPlot,self).draw(layout,subplot)

    def gatherCurves(self,curves):
        vals = OrderedDict()
        for x in curves:
            key = x.data['name']
            if not key in vals:
                vals[key] = []
            vals[key].append(x)
        return vals

summaryplot = SummaryPlot
