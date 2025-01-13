from collections import defaultdict
import copy
from semperpy.plot.plotdirective import PlotDirective
from semperpy.plot.mplib.titles import PlotTitle

class FieldPlot(PlotDirective):

    def distribute(self):
        pass

    def finalise(self):
        pass

    def doRetrieve(self):
        pass

    def dodraw(self,layout,subplot):
        comments = CommentDrawer(self['comment'])
        comments.drawBackground(layout,subplot,self)
        self.draw(layout,subplot)
        comments.drawForeground(layout,subplot,self)

    def draw(self,layout,subplot):
        pass

    def createTextTemplates(self):
        return self.title()

    def plotText(self,owner,layout,subplot,main_title=None):
        text = self.data.createTextTemplate()
        if main_title is None:
            main_title = self.createTextTemplates()
        if self['has_title']:
            self.plotTitle(layout,subplot,main_title,text,self.data)
        self.plotColorbarTitle(layout,subplot,text,info,self.me_)

    def plotTitle(self,layout,subplot,title,text,info):
        PlotTitle()(layout,subplot,text.processText(title,info,section='title'),self['title_font'])

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

fieldplot = FieldPlot
