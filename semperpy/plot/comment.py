from semperpy.core.decorators import abstractMethod
from semperpy.directive.directive import Directive

class Comment(Directive):
    
    @abstractMethod
    def draw(self,layout,subplot,owner,**kargs):
        pass

class CommentDrawer(object):

    def __init__(self,comments):
        self.background_ = [ x for x in comments if x['rank'] < 0 ]
        self.background_.sort()
        self.foreground_ = [ x for x in comments if x['rank'] > 0 ]
        self.foreground_.sort()

    def drawBackground(self,layout,subplot,owner,**kargs):
        self.draw(self.background_,layout,subplot,owner,**kargs)

    def drawForeground(self,layout,subplot,owner,**kargs):
        self.draw(self.foreground_,layout,subplot,owner,**kargs)

    def draw(self,comments,layout,subplot,owner,**kargs):
        for comment in comments:
            comment.draw(layout,subplot,owner,**kargs)
