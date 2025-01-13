from matplotlib import patches

class Rectangle(object):

    def draw(self,layout,subplot,x,y,width,height,linewidth=None,color=None):
        edgecolor = None
        if color is not None: edgecolor = color
        subplot.add_patch(patches.Rectangle((x-(width/2.0),y-(height/2)),width,height,edgecolor=edgecolor,linewidth=linewidth,facecolor='none'))
