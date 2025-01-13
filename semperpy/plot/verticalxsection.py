from semperpy.plot.colorbarplot import ColorbarPlot

class VerticalXSection(ColorbarPlot):

    def finalise(self):
        super(VerticalXSection,self).finalise()
        self['graphics'].horizontal(True)

verticalxsection = VerticalXSection
