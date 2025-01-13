from matplotlib.font_manager import FontProperties
from semperpy.plot.comment import Comment

class CommentText(Comment):

    def draw(self,layout,subplot,owner):
        b = subplot.annotate(self['text'],(self['x'],self['y']),xycoords=self['coords'],fontproperties=FontProperties(**self['font']),color = self['color'],rotation=self['rotation'])
        return b

commenttext = CommentText
