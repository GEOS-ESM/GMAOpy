import copy
import re
from collections import defaultdict
import gc
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#import matplotlib.mpl as mpl
from matplotlib.figure import Figure
import matplotlib.transforms as mtransforms
import matplotlib.gridspec as gridspec
from semperpy.core.tools import tiles2slices

## converting pytohn 2.7 to python 3.11 this was required
## change  
## bboxi = bbox.inverse_transformed(self.fig.transFigure) 
## to 
## bboxi = bbox.transformed(self.fig.transFigure.inverted())
## so every instance of inverse_transformed was changed in this similar way


class Layout(object):

    factory_ = {}

    def __init__(self,geometry,size,interactive = False,layout_tiles = []):
        self.cols_ = geometry[0]
        self.rows_ = geometry[1]
        self.slices_ = layout_tiles
        if len(self.slices_) == 0:
            for i in range(self.rows_):
                for j in range(self.cols_):
                    self.slices_.append((slice(i,i+1),slice(j,j+1)))
        else:
            self.slices_ = tiles2slices(layout_tiles,(self.cols_,self.rows_))
        if len(size) == 0:
            size = None
        elif len(size) == 1:
            size.append(size[0])
        self.gs_ = gridspec.GridSpec(geometry[1],geometry[0])
        self.size_ = size
        self.count_ = 1
        self.pages_ = 1
        self.interactive_ = interactive
        self.flushed_ = False
        self.actions_ = None
        self.subplots_ = []
        self.figure_ = None
        self.canvas_ = None
        self.clearActions()
        self.figure_ = self.newFigure(1)

    def clearActions(self):
        del(self.actions_)
        self.actions_ = defaultdict(list)
        self.bag_ = {}
        self.actor_ = None

    def fullPage(self):
        return self.count_ > len(self.slices_)

    def remaining(self):
        return self.count_ > 1 and not self.flushed_

    def __call__(self):
        self.flushed_ = False
        if self.fullPage():
            self.count_ = 1
            self.pages_ += 1
            self.figure_ = self.newFigure(self.pages_)
        slices = self.slices_[self.count_-1]
        subplot = self.figure_.add_subplot(self.gs_[slices[0],slices[1]])
        self.positions_[subplot] = (slices[0],slices[1])
        self.subplots_.append(subplot)
        self.count_ += 1
        return subplot

    def newFigure(self,page):
        self.clearActions()
        self.positions_ = {}
        while len(self.subplots_) > 0:
            subplot = self.subplots_.pop(0)
            del(subplot)
        # call to figure.clear() was found on stackoverflow
        # it delete the memory used by the figure
        if self.figure_ is not None:
            self.figure_.clear()
            del(self.figure_)
        del(self.canvas_)
        if self.interactive_:
            import matplotlib.pyplot as plt
            self.figure_ = plt.figure(figsize=self.size_)
            self.figure_.canvas.mpl_connect('draw_event',self.on_draw)
            return self.figure_
        else:
            self.figure_ = Figure(figsize=self.size_)
            self.canvas_ = FigureCanvas(self.figure_)
            self.canvas_.mpl_connect('draw_event',self.on_draw)
        # it is a good idea to now invoke the garbage collector
        gc.collect()
        return self.figure_

    def draw(self,filename = 'plot.png'):
        if self.interactive_:
            import matplotlib.pyplot as plt
            plt.show()
        else:
            self.canvas_.print_figure(filename)
        self.flushed_ = True

    def registerDrawingAction(self,action,priority=100,**kargs):
        kargs['figure'] = self.figure_
        if callable(action):
            kargs['action'] = action
        else:
            kargs['action'] = self.factory_[action]()
        self.actions_[priority].append(kargs)

    @classmethod
    def registerAction(self,name,action):
        self.factory_[name] = action

    def on_draw(self,event):

        class DrawActor(object):
            
            def __init__(self,actions,bag,positions):
                self.bag_ = bag
                self.positions_ = positions
                priorities = list(actions.keys())
                priorities.sort()
                self.actions_ = []
                for p in priorities:
                    self.actions_.append(list(actions[p]))

            def __call__(self,event):
                redraw = False
                actions = self.actions_[0]
                for action in actions:
                    if action['action'] is not None:
                        #print action['action']
                        draw = action['action'](event,self.bag_,self.positions_,**action)
                        if not draw:
                            action['action'] = None
                        redraw = redraw or draw
                if not redraw:
                    self.actions_ = self.actions_[1:]
                return redraw

            def actions(self):
                return len(self.actions_) > 0

        # avoid infinite recursion at the end
        if self.actor_ is None:
            self.actor_ = DrawActor(self.actions_,self.bag_,self.positions_)
        while self.actor_.actions():
            redraw = self.actor_(event)
            if redraw:
               self.figure_.canvas.draw()
        return False

    def legend(self,subplot,lines,texts,**kargs):
        linecount = len(texts)
        if not 'ncol' in kargs:
            ncols = linecount
            if ncols > 4:
                ncols = linecount // 2
            kargs['ncol'] = ncols
        alpha = 1.0
        if 'alpha' in kargs:
            alpha = kargs['alpha']
            del(kargs['alpha'])
        legend = subplot.legend(lines,texts,**kargs)
        # make legend transparent
        legend.get_frame().set_alpha(alpha)

    def claimNewAxes(self,parent,rect,left = 0,top = 0,right = 0,bottom = 0,position = 'right',create = True,padding = 0.015):
        bounds = parent.get_window_extent()
        bounds = bounds.transformed(self.figure_.transFigure.inverted())
        rect = copy.copy(rect)
        if rect[2] == 0:
            rect[3] = bounds.x1 - bounds.x0
        if rect[3] == 0:
            rect[3] = bounds.y1 - bounds.y0
        if position == 'left':
            left += bounds.x0
            rect[0] = left - padding
            self.figure_.subplots_adjust(left=left)
        elif position == 'right':
            right = bounds.y1 - right
            rect[0] = right + padding
            self.figure_.subplots_adjust(right=right)
        elif position == 'top':
            top = bounds.x1 - top
            rect[1] = top - padding
            self.figure_.subplots_adjust(top=top)
        elif position == 'bottom':
            bottom += bounds.y0
            rect[1] = bottom + padding
            self.figure_.subplots_adjust(bottom=bottom)
        ax = None
        #rect = [rect[0], rect[1], rect[2]-0.005, rect[3]]
        if create:
            ax = self.figure_.add_axes(rect)
        return rect,ax

    def findGroupedTextObjects(self,subplot,id):
        seen = set()
        def findText(x):
            if isinstance(x,matplotlib.text.Text):
                text = x.get_text()
                if len(text) > 0 and hasattr(x,'get_gid') and x.get_gid() == id:
                    if not x in seen:
                        series['%s' % id].append(x)
                        seen.add(x)
            return False
        series = defaultdict(list)
        subplot.findobj(findText)
        return series


class Spacer(object):
    padding_ = 1.1
    def __init__(self):
        self.current_ = 0

class YLabelSpace(Spacer):

    maxwidth_ = 0

    def __init__(self):
        self.current_ = 0

    def __call__(self,event,bag,positions,subplot=None,figure=None,**kargs):
        redraw = False
        if self.current_ >= 1:
            return False
        self.current_ += 1
        bboxes = []
        title = subplot.yaxis.get_label_text()
        if title != '':
            title = subplot.yaxis.get_label()
            bbox = title.get_window_extent(renderer = event.renderer)
            bboxes.append(bbox.transformed(figure.transFigure.inverted()))
        xticks = subplot.get_yticklabels()
        for tick in xticks:
            bbox = tick.get_window_extent(renderer = event.renderer)
            bboxi = bbox.transformed(figure.transFigure.inverted())
            bboxes.append(bboxi)
        if len(bboxes) > 0:
            bbox = mtransforms.Bbox.union(bboxes)
            if bbox.width > YLabelSpace.maxwidth_:
                YLabelSpace.maxwidth_ = bbox.width
            if bbox.width * self.padding_ > figure.subplotpars.left:
                figure.subplots_adjust(left=self.padding_*bbox.width)
                redraw = True
        return redraw

class XLabelSpace(Spacer):
    def __call__(self,event,bag,positions,subplot=None,figure=None,**kargs):
        redraw = False
        if self.current_ >= 1:
            return False
        self.current_ += 1
        bboxes = []
        title = subplot.xaxis.get_label_text()
        if title != '':
            title = subplot.xaxis.get_label()
            bbox = title.get_window_extent(renderer = event.renderer)
            bboxes.append(bbox.transformed(figure.transFigure.inverted()))
        xticks = subplot.get_xticklabels()
        for tick in xticks:
            bbox = tick.get_window_extent(renderer = event.renderer)
            bboxi = bbox.transformed(figure.transFigure.inverted())
            bboxes.append(bboxi)
        if len(bboxes) > 0:
            bbox = mtransforms.Bbox.union(bboxes)
            if bbox.height * self.padding_ + 0.02 > figure.subplotpars.bottom:
                figure.subplots_adjust(bottom=self.padding_*bbox.height + 0.02)
                redraw = True
        return redraw

class PlotTitleSpace(Spacer):
    def __call__(self,event,bag,positions,subplot=None,figure=None,title=None,**kargs):
        if self.current_ > 0:
            return False
        self.current_ += 1
        redraw = False
        bbox = title.get_window_extent(renderer = event.renderer)
        bboxi = bbox.transformed(figure.transFigure.inverted())
        bag['titleBottom'] = 1-bboxi.height - 0.015
        bag['title'] = title
        if bboxi.y1 > 1:
            figure.subplots_adjust(top=bag['titleBottom'])
            redraw = True
        return redraw

class MainPlotTitleSpace(Spacer):
    def __call__(self,event,bag,positions,subplot=None,figure=None,title=None,**kargs):
        redraw = False
        if self.current_ >= 1:
            return False
        self.current_ += 1
        bbox = title.get_window_extent(renderer = event.renderer)
        bboxi = bbox.transformed(figure.transFigure.inverted())
        bag['titleBottom'] = bboxi.y0 - 0.01
        bag['title'] = title
        figure.subplots_adjust(top = bag['titleBottom'])
        redraw = True
        return redraw

class AdjustTickLabelSize(object):
    sizes_ = ('xx-small', 'x-small', 'small')
    def __init__(self):
        self.current_ = len(self.sizes_)
        self.done_ = False

    def __call__(self,event,bag,positions,subplot=None,figure=None,**kargs):
        redraw = False
        if not self.done_ and self.current_ != 0:
            ticks = [ x for x in self.ticks(subplot) if x.get_text() != '' ]
            bboxes = []
            for tick in ticks:
                # if the tick labels are rotated, their bounding boxes can overlap
                # without the text overlapping. So in that case we do nothing.
                if tick.get_rotation() != 0:
                    self.done_ = True
                    return False
                bbox = tick.get_window_extent(renderer = event.renderer)
#                bbox = bbox.inverse_transformed(figure.transFigure)
                bbox = bbox.transformed(figure.transFigure.inverted())
                bboxes.append(bbox)
            reduce = False
            for i in range(1,len(bboxes)):
                if self.overlap(bboxes[i],bboxes[i-1]):
                    reduce = True
                    break
            if reduce:
                self.current_ -= 1
                if self.current_ >= 0:
                    for tick in ticks:
                        tick.set_size(self.sizes_[self.current_])
                    redraw = True
                else:
                    self.done_ = True
            else:
                self.done_ = True
        return redraw

class AdjustXTickLabelSize(AdjustTickLabelSize):
    def ticks(self,subplot):
        return subplot.get_xticklabels()

    def overlap(self,a,b):
        return a.x0 < b.x1

class AdjustYTickLabelSize(AdjustTickLabelSize):
    def ticks(self,subplot):
        return subplot.get_yticklabels()

    def overlap(self,a,b):
        return a.y0 < b.y1

class ColorBarSpace(object):

    def __init__(self):
        self.done_ = False

    def __call__(self,event,bag,positions,ax=None,subplot=None,colorbar=None,figure=None,**kargs):
        if self.done_:
            return False
        else:
            bounds = ax.get_window_extent(renderer = event.renderer)
            bounds = bounds.transformed(figure.transFigure.inverted())
            bboxes = []
            for x in ax.findobj(self.findText):
                bbox =  x.get_window_extent(renderer = event.renderer)
                bboxes.append(bbox.transformed(figure.transFigure.inverted()))
            if len(bboxes) > 0:
                bbox = mtransforms.Bbox.union(bboxes)
                parent = subplot.get_window_extent(renderer = event.renderer)
                parent = parent.transformed(figure.transFigure.inverted())
                height = parent.y1-parent.y0
                position = positions[subplot]
                if position[0].start == 0 and 'titleBottom' in bag:
                    height = bag['titleBottom'] - parent.y0
                shift =  (bbox.x1 - 1) + 0.015
                figure.subplots_adjust(right = bounds.x0 - shift - 0.015)
                ax.set_position([bounds.x0 - shift,parent.y0,bounds.x1-bounds.x0,height])
            self.done_ = True
        return True

    def findText(self,x):
        if isinstance(x,matplotlib.text.Text):
            return True
        return False

class ColorBarTextSize(ColorBarSpace):

    def __call__(self,event,bag,positions,ax=None,subplot=None,colorbar=None,figure=None,title_size=None,tick_label_size=None,**kargs):
        if self.done_:
            return False
        else:
            # this only works for a vertical bar, might need to be extended to the general case
            for x in ax.findobj(self.findText):
                if x.get_rotation() == 90.0:
                    x.set_size(title_size)
                elif x.get_rotation() == 0.0:
                    x.set_size(tick_label_size)
            self.done_ = True
        return True

class SetRatio(Spacer):
    def __call__(self,event,bag,positions,subplot=None,figure=None,ratio=None,**kargs):
        if self.current_ > 0:
            return False
        self.current_ += 1
        bbox = subplot.get_window_extent(renderer = event.renderer)
        bboxi = bbox.transformed(figure.transFigure.inverted())
        bboxi = bbox
        figure.subplots_adjust(right=bboxi.x0 + (bboxi.y1 - bboxi.y0) * ratio)
        return True

class PlaceLegend(Spacer):

    def __call__(self,event,bag,positions,subplot=None,figure=None,position=None,vertical_offset = 0,**kargs):
        if self.current_ > 0:
            return False
        self.current_ += 1
        
        bbox = subplot.get_window_extent(renderer = event.renderer)
        bbox = bbox.transformed(figure.transFigure.inverted())
        legend = subplot.get_legend()
        legendBox = legend.get_window_extent()
        legendBox = legendBox.transformed(figure.transFigure.inverted())
        bboxes = [ x.get_window_extent() for x in legend.get_texts() ]
        textbbox = mtransforms.Bbox.union(bboxes)
        #print('TEXT BBOX TEST', textbbox, type(textbbox))
        textbbox = textbbox.transformed(figure.transFigure.inverted())
        #print(textbbox, type(textbbox))
        height = textbbox.height * 1.1 / bbox.height
        if position == 'top':
            #print(bbox.height)
            #print(type(vertical_offset))
            #print([bbox.x0,bbox.y0,bbox.width,bbox.height-vertical_offset])
            #print('BBOX PRINT CHECK', (0.5,1.0 + height + vertical_offset))
            subplot.set_position([bbox.x0,bbox.y0,bbox.width,bbox.height])
            #subplot.set_position([bbox.x0,bbox.y0,bbox.width,bbox.height*0.98-vertical_offset])
            #legend.set_bbox_to_anchor((0.5,1.0 + height + vertical_offset))
        elif position == 'bottom':
            subplot.set_position([bbox.x0 + height/2,bbox.y0,bbox.width,bbox.height-height/2])
            #legend.set_bbox_to_anchor((0.5,-height-vertical_offset ))
        elif position == 'topleft':
            subplot.set_position([bbox.x0,bbox.y0,bbox.width,bbox.height-vertical_offset])
            #legend.set_bbox_to_anchor((bbox.x0,1 + height + vertical_offset ))
        elif position == 'bottomleft':
            subplot.set_position([bbox.x0 + height/2,bbox.y0,bbox.width,bbox.height-height/2])
            #legend.set_bbox_to_anchor((bbox.x0,-height -vertical_offset ))
        return True

class AdjustTitle(Spacer):

    def __call__(self,event,bag,positions,subplot=None,figure=None,position=None,**kargs):
        if self.current_ > 0:
            return False
        self.current_ += 1
        
        title = bag['title']
        bbox = title.get_window_extent(renderer = event.renderer)
        bboxi = bbox.transformed(figure.transFigure.inverted())
        title.set_y(1.0+1.0-bboxi.y1)
        return True

class AlignYLabels(Spacer):

    def __call__(self,event,bag,positions,subplot=None,figure=None,layout = None,**kargs):
        if self.current_ > 0:
            return False
        self.current_ += 1
        if len(layout.subplots_) > 1:
            for subplot in layout.subplots_:
                subplot.yaxis.set_label_coords(-YLabelSpace.maxwidth_* 1.1,0.5)
        return True

class SpreadTextVertically(Spacer):

    def __call__(self,event,bag,positions,subplot=None,figure=None,layout = None,id=None,**kargs):
        def sortBoxes(a,b):
            # sort items from top to bottom
            aa = a.get_window_extent()
            bb = b.get_window_extent()
            return cmp(bb.y0,aa.y0)

        if self.current_ > 0:
            return False
        self.current_ += 1
        series = layout.findGroupedTextObjects(subplot,id)
        for group in series.values():
            group.sort(sortBoxes)
            for i in range(len(group)):
                obj2 = group[i]
                box2 = obj2.get_window_extent()
                if i > 0:
                    obj1 = group[i-1]
                    box1 = obj1.get_window_extent()
                    offset = box1.y0 - box2.y1
                else:
                    offset = 0
                pos = subplot.transData.transform(obj2.get_position())
                pos[0] += 3
                if offset < 0:
                    pos[1] += offset - 3
                pos = subplot.transData.inverted().transform(pos)
                obj2.set_position(pos)
        return True

Layout.registerAction('MakeSpaceForXLabels',XLabelSpace)
Layout.registerAction('MakeSpaceForYLabels',YLabelSpace)
Layout.registerAction('MakeSpaceForTitle',PlotTitleSpace)
Layout.registerAction('MakeSpaceForMainTitle',MainPlotTitleSpace)
Layout.registerAction('MakeSpaceForColorBar',ColorBarSpace)
Layout.registerAction('ColorBarTextSize',ColorBarTextSize)
Layout.registerAction('AdjustXTickLabelSize',AdjustXTickLabelSize)
Layout.registerAction('AdjustYTickLabelSize',AdjustYTickLabelSize)
Layout.registerAction('SetRatio',SetRatio)
Layout.registerAction('PlaceLegend',PlaceLegend)
Layout.registerAction('AlignYLabels',AlignYLabels)
Layout.registerAction('SpreadTextVertically',SpreadTextVertically)
Layout.registerAction('AdjustTitle',AdjustTitle)
