from matplotlib.font_manager import FontProperties

class GraphicalText(object):
    titlesize_ = ['','large','medium','small','x-small','xx-small','xx-small']

class PlotTitle(GraphicalText):
    
    def __call__(self,layout,subplot,title,font = None):
        if font.isDefault('size'):
            font['size'] = self.titlesize_[layout.cols_]
        title = subplot.set_title(title,fontproperties = FontProperties(**font))
        layout.registerDrawingAction('MakeSpaceForTitle',subplot = subplot, title = title)


class MainTitle(GraphicalText):
    
    def __call__(self,layout,subplot,title,font = None):
        title = subplot.annotate(title,(0.5,1.0),xycoords='figure fraction',horizontalalignment = 'center',verticalalignment='top',size='large',fontproperties = FontProperties(**font))
        layout.registerDrawingAction('MakeSpaceForMainTitle',figure = layout.figure_,subplot = subplot, title = title)


class XAxisTitle(object):

    def __call__(self,layout,subplot,title,size):
        subplot.xaxis.set_label_text(title,size=size)
        

class YAxisTitle(object):

    def __call__(self,layout,subplot,title,size):
        subplot.yaxis.set_label_text(title,size=size)
