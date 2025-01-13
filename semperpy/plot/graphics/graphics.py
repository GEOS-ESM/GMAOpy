from semperpy.core.tools import is_string
from semperpy.plot.graphics.attribute import Attribute
from semperpy.plot.graphics.plotstyle import PlotStyle

class AttributeIterator(object):

    def __init__(self,attr):
        self.attr_ = attr
        self.index_ = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index_ += 1
        if self.index_ == len(self.attr_):
            self.index_ = 0
        return self.attr_[self.index_]

    def __getitem__(self,index):
        index = index % len(self.attr_)
        return self.attr_[index]
        

class Graphics(Attribute):

    def __init__(self,*args,**kargs):
        super(Graphics,self).__init__(*args,**kargs)
        self.done_ = False

    def checkLanguage(self,*args,**kargs):
        if not self.done_:
            super(Graphics,self).checkLanguage(*args,**kargs)
            for category in self['_categories']:
                color = category + '_color'
                if color in self:
                    newcolors = []
                    for col in self[color]:
                        newcolors.append(PlotStyle.colors[col])
                    self[color] = newcolors
            if 'style' in self:
                newstyles = []
                for style in self['style']:
                    newstyles.append(PlotStyle.linestyles[style])
                self['style'] = newstyles
            self.done_ = True

    def colors(self,category):
        colors = self[category + '_color']
        if is_string(colors):
            colors = self[self[category + '_color']]
        return AttributeIterator(colors)
    
    def styles(self):
        return AttributeIterator(self['style'])

class VertGraphics(Graphics):
    pass

graphics = Graphics
vertgraphics = VertGraphics
