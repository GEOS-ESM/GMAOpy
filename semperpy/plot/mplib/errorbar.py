from matplotlib import patches

class ErrorBar(object):

    def draw(self,layout,subplot,x,y,width,height,linewidth=None,color=None):
        ecolor = None
        if color is not None: ecolor = color
        elinewidth = None
        if linewidth is not None: elinewidth = linewidth
        subplot.errorbar(x,y,yerr=height/2,ecolor=ecolor,elinewidth=elinewidth)
