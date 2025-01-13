from collections import OrderedDict
import copy
from matplotlib.ticker import IndexLocator
from semperpy.core.tools import to_list, is_tuple
from semperpy.core.date import Date
from semperpy.plot.dimension import Dimension
from gmaopy.obs.obstexttemplate import ObsTextTemplate

class LevelXSectionDimension(Dimension):

    def prepare_values(self,data,values):
        if 'levtype' in data:
            t = data['levtype']
            rev = True
            if t == 'sfc' or t == 'ch' or t == 'wl':
                rev = False
            if is_tuple(values):
                values = list(values)
            values.sort(reverse = rev)
        return values

    def process_values(self,values,*args):
        return values

    def process_axis(self,layout,subplot,axis,values,curves):
        axis.min(values[0])
        axis.max(values[-1])
        axis.scale('log')
        labels = self.labels_for_float(values)
        axis(layout,subplot,labels=labels,ticks=values)

class LevelPlotDimension(Dimension):

    """
        A bit of a mess here with pressure levels, depth, channels etc...
        prepare_values sort the values of levels in the order we want to
        have them before retrieving the data. For a level plot, we end up
        with an array of N values, the first value is at the bottom of the
        plot.
    """

    def prepare_values(self,data,values):
        if 'levtype' in data:
            t = data['levtype']
            rev = True
            if t == 'sfc' or t == 'ch' or t == 'wl':
                rev = False
            if is_tuple(values):
                values = list(values)
            values.sort(reverse = rev)
        return values

    def process_values(self,values,curves):
        values = to_list(values)
        v = list(range(len(values)))
        return v

    def levtype(self,curves):
        all = set()
        for curve in curves:
            for t in to_list(curve.data['levtype']):
                all.add(t)
        return all

    def process_axis(self,layout,subplot,axis,values,curves):

        axis_values = self.process_values(values,curves)
        major_locator = None
        if len(values) > 100:
            div = 20
        elif len(values) > 50:
            div = 10
        elif len(values) > 30:
            div = 5
        else:
            div = 1
        if div != 1:
            vals = []
            for i in list(range(len(values))):
                if (values[i] % div) == 0 or i == 0:
                    vals.append(values[i])
            values = vals
            major_locator = IndexLocator(div,0)
        labels = self.labels_for_float(values)
        '''
        if 'absolute_max' in axis:
            if len(values) < axis['absolute_max']:
                axis = copy.copy(axis)
                axis['max'] = axis['absolute_max']
                axis_values = [-1] + axis_values
                values = [values[0] +1] + values
                if not axis['horizontal']:
                    subplot.axvline(x = 0,color='black',linewidth=0.8)
                else:
                    subplot.axhline(y = 0,color='black',linewidth=0.8)
                labels = self.labels_for_float(values)
                labels[0] = ''
        '''
        axis(layout,subplot,labels=labels,ticks=axis_values,maj_locator=major_locator)

class ChannelPlotDimension(LevelPlotDimension):
    
    def levtype(self,curves):
        return set(['ch'])

class WaveLengthPlotDimension(LevelPlotDimension):
    
    def levtype(self,curves):
        return set(['wl'])

class SummaryPlotDimension(Dimension):

    def process_axis(self,layout,subplot,axis,values,curves):
        d = OrderedDict()
        vals = [ x.data['name'] for x in curves ]
        for v in vals:
            d[v] = 1
        vals = d.keys()
        text = ObsTextTemplate()
        labels = [ text.getText('name',dict(name=x),'title') for x in vals ]
        axis(layout,subplot,labels=labels)

class ODSSummaryPlotDimension(Dimension):
    
    def process_axis(self,layout,subplot,axis,values,curves):
        axis_values = self.process_values(values,curves)
        d = OrderedDict()
        vals = [ x.data['name'] for x in curves ]
        for v in vals:
            d[v] = 1
        vals = d.keys()
        text = ObsTextTemplate()
        if 'absolute_max' in axis:
            if len(values) < axis['absolute_max']:
                axis = copy.copy(axis)
                axis['max'] = axis['absolute_max']
                if not axis['horizontal']:
                    subplot.axvline(x = 0,color='black',linewidth=0.8)
                else:
                    subplot.axhline(y = 0,color='black',linewidth=0.8)
                axis_values = [-1] + list(range(len(axis_values)))
            labels = [''] + [ text.getText('name',dict(name=x),'title') for x in vals ]
        else:
            labels = [ text.getText('name',dict(name=x),'title') for x in vals ]
        axis(layout,subplot,labels=labels,ticks=axis_values)

Dimension.register('level','verticalxsection',LevelXSectionDimension)
Dimension.register('level','levelplot',LevelPlotDimension)
Dimension.register('level','odslevelplot',LevelPlotDimension)
Dimension.register('level','channelplot',ChannelPlotDimension)
Dimension.register('level','wavelengthplot',WaveLengthPlotDimension)
Dimension.register('name','summaryplot',SummaryPlotDimension)
Dimension.register('name','odssummaryplot',ODSSummaryPlotDimension)
