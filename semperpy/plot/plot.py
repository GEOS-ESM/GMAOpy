import copy
from collections import defaultdict, OrderedDict
from semperpy.core.tools import no_list,is_list,to_list,classname
from semperpy.plot.plotdirective import PlotDirective
from semperpy.plot.curve import Curve
from semperpy.plot.mplib.titles import PlotTitle,XAxisTitle,YAxisTitle
from semperpy.plot.document import Document
from semperpy.plot.comment import CommentDrawer
from semperpy.plot.dimension import Dimension
import functools

def cmp(x,y):
    if x < y:
        return -1
    elif x > y:
        return 1
    else:
        return 0

def sortIncreasing(a,b):
    return cmp(b.data.value[0],a.data.value[0])

def sortDecreasing(a,b):
    return cmp(a.data.value[0],b.data.value[0])

def sortRankIncreasing(a,b):
    #aval = min([ int(x.data.get('rank',100000)) for x in a ])
    #bval = min([ int(x.data.get('rank',100000)) for x in b ])
    aval = min([int(a.get('plotdata').get('rank',100000))])
    bval = min([int(b.get('plotdata').get('rank',100000))])
    return cmp(bval,aval)

def sortRankDecreasing(a,b):
    #aval = max([ int(x.data.get('rank',-1)) for x in a ])
    #bval = max([ int(x.data.get('rank',-1)) for x in b ])
    aval = max([int(a.get('plotdata').get('rank',-1))])
    bval = max([int(b.get('plotdata').get('rank',-1))])
    return cmp(aval,bval)


class Plot(PlotDirective):

    sort_ = dict(
        decreasing = sortDecreasing,
        increasing = sortIncreasing,
        rank_decreasing = sortRankDecreasing,
        rank_increasing = sortRankIncreasing,
    )
    legendsize_ = ['','medium','medium','small','x-small','xx-small','xx-small'] + ['xx-small'] * 15

    def distribute(self):
        if 'datahook' in self:
            Document.silent_ = True
        self.curves_ = self.distributeCurves(self['curve'],self.me_)

    def distributeCurves(self,curves,name):
        combinations = []
        for curve in curves:
            curve = copy.copy(curve)
            curve.overwrite_from(self,exclude='filename')
            all = curve.data.distribute(self,name)
            for one in all:
                c = copy.copy(curve)
                c.data = one
                c.finalise()
                combinations.append(c)
        return combinations

    def finalise(self):
        self['xaxis'].setHorizontal()
        self.checkCurvePreferences()
        # just so that it prints out the right
        # information
        self['curve'] = self.curves_

    def doRetrieve(self):
        for curve in self.curves_:
            curve.startRetrieve()
        for curve in self.curves_:
            curve.doRetrieve(self,self.me_)
        for curve in self.curves_:
            curve.stopRetrieve()

    def sortCurves(self,curves):
        sort = self['sort']
        if sort is not None:
#            curves.sort(self.sort_[sort])
            curves = sorted(curves,key=functools.cmp_to_key(self.sort_[sort]))
        return curves
        
    def checkCurvePreferences(self):
        for curve in self.curves_:
            if curve.isDefault('kind'):
                curve.kind = self['_curve_preference']

    def dodraw(self,layout,subplot):
        self.feedObservers()
        layout.registerDrawingAction('AdjustXTickLabelSize',subplot = subplot)
        layout.registerDrawingAction('AdjustYTickLabelSize',subplot = subplot)
        layout.registerDrawingAction('MakeSpaceForXLabels',subplot = subplot)
        layout.registerDrawingAction('MakeSpaceForYLabels',subplot = subplot)
        layout.registerDrawingAction('AlignYLabels',subplot = subplot, layout = layout, priority = 500)
        comments = CommentDrawer(self['comment'])
        comments.drawBackground(layout,subplot,self)
        self.draw(layout,subplot)
        comments.drawForeground(layout,subplot,self)

    def feedObservers(self):
        observers = self.data.get('observer',[])
        for curve in self.curves_:
            all = curve.feedObservers(self.data,observers)
            for k,i in all.items():
                if not k in self.data:
                    self.data[k] = i
        for observer in observers:
            self.data[observer.varname()] = observer.value()

    def dispatchGraphicsAttributes(self,category):
        colors = self['graphics'].colors(category)
        styles = self['graphics'].styles()
        for curve in self.curves_:
            curve['graphics'] = copy.copy(curve['graphics'])
            if not 'color' in curve['graphics']:
                curve['graphics']['color'] = next(colors)
            if not 'style' in curve['graphics']:
                curve['graphics']['style'] = next(styles)
            else:
                curve['graphics']['style'] = no_list(curve['graphics']['style'])

    def draw(self,layout,subplot):
        if len(self.curves_) == 0:
            return
        axis_name = self.data.draw_index_columns(self.me_)
        if len(axis_name) > 1:
            raise SystemError('Cannot handle more than one dimension at the moment')
        # gather all values on the indexed dimension (e.g date for timeseries, level for xsection)
        axis_name = axis_name[0]
        index_values = OrderedDict()
        values = []
        for curve in self.curves_:
            data = curve.data
            axis_names = to_list(data[axis_name])
            for value in axis_names:
                #for date in value:
                #index_values[int(str(value[0])[:-2])] = 0
                index_values[value] = 0
            for v in data.value:
                values.append(v)

        index_values = list(index_values.keys())
        # gather all values on the other dimension (the actual values)
        if self['graphics'].grid():
            subplot.grid(True, linestyle=':')
        index_dimension = Dimension.createDimensionFilter(axis_name,self.me_)
        dimension = Dimension.createDimensionFilter('',self.me_)
        categories = defaultdict(list)
        self.curves_ = self.eliminateMissing(self.curves_)
        for curve in self.curves_:
            category = curve.kind
            categories[category].append(curve)
        for category,curves in list(categories.items()):
            categories[category] = self.sortCurves(curves) 
        drawers = []
        minv = None
        maxv = None
        allmissing = True
        for category,curves in categories.items():
            self.dispatchGraphicsAttributes(category)
            drawer = Curve.createDrawer(category,curves)
            drawers.append(drawer)
            min,max,missing = drawer.calculateMinMax([ x.data for x in curves ])
            if minv == None or min < minv:
                minv = min
            if maxv == None or max > maxv:
                maxv = max
            #print('MIN CHECK', allmissing, missing, allmissing and missing)
            allmissing = allmissing and missing
        process_axis = True
        for drawer,curves in zip(drawers,categories.values()):
            if process_axis:
                process_axis = False
                if self['graphics'].horizontal():
                    index_dimension.process_axis(layout,subplot,self['yaxis'],index_values,curves)
                    axis = copy.copy(self['xaxis'])
                    axis = self.assignMinMax(minv,maxv,axis,allmissing)
                    dimension.process_axis(layout,subplot,axis,values,curves)
                else:
                    index_dimension.process_axis(layout,subplot,self['xaxis'],index_values,curves)
                    axis = copy.copy(self['yaxis'])
                    axis = self.assignMinMax(minv,maxv,axis,allmissing)
                    dimension.process_axis(layout,subplot,axis,values,curves)
            lines = drawer.draw(layout,subplot,dimension = index_dimension,axis_name=axis_name,owner = self,**self['graphics'])
            for i,line in enumerate(lines):
                curves[i]['_graph_'] = line
            if 'datahook' in self:
                self.datahook(axis_name,[ x.data for x in curves ],self['datahook'])

    def eliminateMissing(self,curves):
        """
            In some cases (e.g. when diplaying bars), we prefer not to display bars for entries with only
            missing values. By default we keep everything, subclasses may remove curves if not wanted:
            example:
                return [ x for x in self.curves if x.data.value ... is to be kept ]
        """
        return curves
    
    def assignMinMax(self,minv,maxv,axis,allmissing):
        if 'min' in axis:
            minv = axis['min']
        if 'max' in axis:
            maxv = axis['max']
        if 'step' in axis:
            step = axis['step']
        if minv == maxv:
            if minv is None:
                minv = None
            else:
                minv = min(0.0,minv)
            if maxv is None:
                maxv = None
            else:
                maxv = max(0.0,maxv)
        if allmissing:
            step = 0
        else:
            step = (maxv - minv) / len(self['curve'][0].data.value)
            minv -= (maxv - minv) * axis['min_bound_padding']
            maxv += (maxv - minv) * axis['max_bound_padding']
            if maxv == minv:
                minv -= minv * 0.05
                maxv += maxv * 0.05
        if not 'min' in axis:
            axis['min'] = minv
        if not 'max' in axis:
            axis['max'] = maxv
        if not 'step' in axis:
            axis['step'] = step
        return axis

    def createTextTemplates(self):
        text = self.data.createTextTemplate()
        legend = self.legend()
        title = self.title()
        main_title = title
        legends = []
        if self['has_legend']:
            maxlen = 0
            for curve in self.curves_:
                if 'user_legend' in curve:
                    legend = curve['user_legend']
                t,l = text.dispatchVariables(title,legend,self.data)
                legends.append(l)
                if len(t) > maxlen:
                    maxlen = len(t)
                    main_title = t
        return main_title,legends

    def createTitleInfo(self):
        return self.data.mergeDirective(x.data for x in self['curve'])

    def plotText(self,owner,layout,subplot,main_title=None,legends=None):
        text = self.data.createTextTemplate()
        if main_title==None:
            main_title,legends = self.createTextTemplates()
        if self['has_legend']:
            self.plotLegend(layout,subplot,legends,text)
        info = self.createTitleInfo()
        if self['has_title']:
            self.plotTitle(layout,subplot,main_title,text,info)
        if self['has_xtitle']:
            self.plotXAxisTitle(layout,subplot,text,info)
        if self['has_ytitle']:
            self.plotYAxisTitle(layout,subplot,text,info)
        self.plotColorbarTitle(layout,subplot,text,info,self.me_)

    def plotLegend(self,layout,subplot,legends,text):
        labels = [ x['_graph_'] for x in self.curves_ if '_graph_' in x ]
        lines = []
        for i in range(len(labels)):
            done = self.curves_[i].generateLegend(layout,subplot,legends[i],text)
            if done != '':
                lines.append(done)
        if len(lines) > 0:
            legend = copy.copy(self['legend'])
            if legend['prop'].isDefault('size'):
                legend['prop']['size'] = self.legendsize_[len(lines)]
            if legend['loc'] == 'outside top':
                legend['loc'] = 'upper center'
                layout.registerDrawingAction('PlaceLegend',subplot=subplot,layout=layout,position = 'top',vertical_offset=legend['vertical_offset'],priority=250)
                layout.registerDrawingAction('AdjustTitle',subplot=subplot,priority=10000)
            elif legend['loc'] == 'outside bottom':
                legend['loc'] = 'lower center'
                legend['bbox_to_anchor'] = (0.5, -0.45)
                layout.registerDrawingAction('PlaceLegend',subplot=subplot,layout=layout,position = 'bottom',vertical_offset=legend['vertical_offset'],priority=250)
            elif legend['loc'] == 'outside topleft':
                legend['loc'] = 'upper left'
                layout.registerDrawingAction('PlaceLegend',subplot=subplot,layout=layout,position = 'topleft',vertical_offset=legend['vertical_offset'],priority=250)
            elif legend['loc'] == 'outside bottomleft':
                legend['loc'] = 'lower left'
                layout.registerDrawingAction('PlaceLegend',subplot=subplot,layout=layout,position = 'bottomleft',vertical_offset=legend['vertical_offset'],priority=250)
            legend = legend.make_kwargs()
            layout.legend(subplot,labels,lines,**legend)
        # need to remove references to the lines (or bars) otherwise matploblib won't
        # release the memory held
        for curve in self.curves_:
            if '_graph_' in curve:
                del(curve['_graph_'])

    def plotTitle(self,layout,subplot,title,text,info):
        PlotTitle()(layout,subplot,text.processText(title,info,section='title'),self['title_font'])

    def plotXAxisTitle(self,layout,subplot,text,info):
        xtitle = self.title_item('xtitle')
        XAxisTitle()(layout,subplot,text.processText(xtitle,info,section='title'),self['xaxis']['title_size'])

    def plotYAxisTitle(self,layout,subplot,text,info):
        ytitle = self.title_item('ytitle')
        YAxisTitle()(layout,subplot,text.processText(ytitle,info,section='title'),self['yaxis']['title_size'])

    def plotColorbarTitle(self,layout,subplot,text,info,what):
        pass

    def title(self):
        template = self.data.title(self.me_)
        if 'title' in self:
            title = self['title']
            for i,v in enumerate(title):
                if v is None:
                    title[i] = template[i]
        else:
            title = template
        return '\n'.join([ x for x in title if x != '' ])

    def title_item(self,which):
        if which in self:
            return self[which]
        method = getattr(self.data,which)
        return method(self.me_)

    def legend(self):
        return self.data.legend(self.me_)

    def __copy__(self):
        new = super(Plot,self).__copy__()
        new.me_ = self.me_
        new.data = copy.copy(self.data)
        return new

    def datahook(self,main_variable,data,what):
        main_values = [ len(to_list(x[main_variable])) for x in data ]
        if len(set(main_values)) != 1:
            raise ValueError('problem with data')
        values = [ len(x.value) for x in data ]
        if len(set(values)) != 1:
            raise ValueError('problem with data')
        new = [ copy.copy(x) for x in data ]
        if values[0] != main_values[0]:
            for i,d in enumerate(new):
                d[main_variable] = d[main_variable][i]
        for d in new:
            for k,i in d.items():
                l = to_list(i)
                d[k] = l
            d['value'] = d.value
        what(main_variable,new)

    def findBiggestSpace(self,subplot,yaxis=True):
        mean = []
        for c in self.curves_:
            mean.append(c.data.value.mean())
        mean.sort()
        if yaxis:
            axis = subplot.yaxis
        else:
            axis = subplot.xaxis
        interval = axis.get_view_interval()
        a1 = mean[0] - interval[0]
        a2 = interval[1] - mean[-1]
        if len(mean) == 1:
            if mean[0] > 0:
                return 1
            else:
                return 0
        elif a1 > a2:
            return 0
        else:
            return 1
    
plot = Plot
