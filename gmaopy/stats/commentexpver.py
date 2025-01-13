from collections import defaultdict
import matplotlib.dates as md
from matplotlib.font_manager import FontProperties
import matplotlib.transforms as mtransforms
from semperpy.core.date import Date
from semperpy.plot.mplib.layout import Layout
from semperpy.plot.comment import Comment

class CommentExpver(Comment):

    textalignment = defaultdict(dict)
    textalignment['top']['indented'] = 'bottom'
    textalignment['top'][''] = 'bottom'
    textalignment['top']['angled'] = 'baseline'
    textalignment['bottom']['indented'] = 'baseline'
    textalignment['bottom'][''] = 'baseline'
    textalignment['bottom']['angled'] = 'bottom'

    def draw(self,layout,subplot,owner):
        curve = list(owner.curves_)[0]
        data = curve.data
        if 'datefile' in data:
            alldates,allexpvers = data.datesAndExpvers(data['datefile'],data['date'])
            if owner['graphics'].horizontal():
                return
            bounds = subplot.yaxis.get_view_interval()
            position = self['position']
            postype = position.split('_')
            prefix = postype[0]
            suffix = ''
            if len(postype) > 1:
                suffix = postype[1]
            if suffix != '' and prefix == 'best':
                if owner.findBiggestSpace(subplot,yaxis = True) == 1:
                    position = 'top_%s' % suffix
                    prefix = 'top'
                else:
                    position = 'bottom_%s' % suffix
                    prefix = 'bottom'
            if prefix == 'top':
                index = 1
            else:
                index = 0
            id = 'commentexpver_%d' % index
            show = set(self['display'])
            for date,expver in zip(alldates,allexpvers):
                dd = md.date2num(Date(date[0]).datetime())
                if 'line' in show:
                    b = subplot.axvline(x=dd,color=self['linecolor'],linestyle=self['style'],alpha=self['alpha'],linewidth=self['linewidth'], dashes=(5,5))
                label = []
                if 'expver' in show:
                    label.append(expver)
                if 'date' in show:
                    d = Date(date[0]).format(self['date_format'])
                    if suffix != 'angled':
                        d = d.strip()
                    label.append(d)
                if len(label) > 0:
                    label = '-'.join(label)
                    t = subplot.text(dd,bounds[index],label,fontproperties=FontProperties(**self['font']),color=self['color'],verticalalignment = self.textalignment[prefix][suffix])
                    t.set_gid(id)
            layout.registerDrawingAction(position,subplot=subplot,id=id,priority=10001,layout=layout,owner=self)

commentexpver = CommentExpver

class AlignExpver(object):

    def __init__(self):
        self.done_ = False

    def __call__(self,event,bag,positions,subplot=None,figure=None,layout = None,id=None,owner=None,**kargs):
        def sortBoxes(a,b):
            # sort items from top to bottom
            aa = a.get_window_extent()
            bb = b.get_window_extent()
            return cmp(aa.x0,bb.x0)

        if self.done_:
            return False
        self.done_ = True
        series = layout.findGroupedTextObjects(subplot,id)
        for group in list(series.values()):
            group.sort(sortBoxes)
            for i,text in enumerate(group):
                previous = None
                if i > 0:
                    previous = group[i-1]
                text = group[i]
                pos = subplot.transData.transform(text.get_position())
                pos = self.adjust_position(owner,text,previous,pos)
                pos = subplot.transData.inverted().transform(pos)
                text.set_position(pos)
        return True

class AlignExpverBottom(AlignExpver):

    def adjust_position(self,owner,text,previous,pos):
        pos[0] += 2
        pos[1] += 4
        return pos

class AlignExpverTop(AlignExpver):

    def adjust_position(self,owner,text,previous,pos):
        box = text.get_window_extent()
        pos[0] += 2
        pos[1] -= box.height + 1
        return pos

class AlignExpverTopIndented(AlignExpver):

    def __init__(self,*args,**kwargs):
        self.shifted_ = set()
        super(AlignExpverTopIndented,self).__init__(*args,**kwargs)

    def adjust_position(self,owner,text,previous,pos):
        box = text.get_window_extent()
        height = box.height
        pos[0] += 2
        pos[1] -= box.height + 2
        if previous is not None:
            prevbox = previous.get_window_extent()
            if prevbox.x1 >= pos[0] and not previous in self.shifted_:
                pos[1] -= box.height
                self.shifted_.add(text)
        return pos

class AlignExpverBottomIndented(AlignExpver):

    def __init__(self,*args,**kwargs):
        self.shifted_ = set()
        super(AlignExpverBottomIndented,self).__init__(*args,**kwargs)

    def adjust_position(self,owner,text,previous,pos):
        box = text.get_window_extent()
        height = box.height
        pos[0] += 2
        pos[1] += 4
        if previous is not None:
            prevbox = previous.get_window_extent()
            if prevbox.x1 >= pos[0] and not previous in self.shifted_:
                pos[1] += box.height
                self.shifted_.add(text)
        return pos

class AlignExpverTopAngled(AlignExpver):

    def adjust_position(self,owner,text,previous,pos):
        box = text.get_window_extent()
        pos[0] += 0
        pos[1] -= box.height - 2
        text.set_rotation(-owner['angle'])
        return pos

class AlignExpverBottomAngled(AlignExpver):

    def adjust_position(self,owner,text,previous,pos):
        box = text.get_window_extent()
        height = box.height
        pos[0] += 2
        pos[1] += 2
        text.set_rotation(owner['angle'])
        return pos

Layout.registerAction('top',AlignExpverTop)
Layout.registerAction('bottom',AlignExpverBottom)
Layout.registerAction('top_indented',AlignExpverTopIndented)
Layout.registerAction('bottom_indented',AlignExpverBottomIndented)
Layout.registerAction('top_angled',AlignExpverTopAngled)
Layout.registerAction('bottom_angled',AlignExpverBottomAngled)
