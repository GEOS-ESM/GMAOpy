from semperpy.plot.comment import Comment

class CommentLine(Comment):

    def draw(self,layout,subplot,owner):
        horizontal = owner['graphics'].horizontal()
        if horizontal:
            b = subplot.axvline(x = self['position'],color=self['color'],linestyle = self['style'],alpha = self['alpha'],linewidth = self['linewidth'], dashes=(5,5))
        else:
            b = subplot.axhline(y = self['position'],color=self['color'],linestyle = self['style'],alpha = self['alpha'],linewidth = self['linewidth'], dashes=(5,5))
        return b

commentline = CommentLine
