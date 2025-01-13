from semperpy.directive import Directive
from semperpy.core.tools import dictionary, substitute_variables
from gmaopy.directives.retrieve import Retrieve
from semperpy.plot.matplotlib import *


class XSection(Directive):

    dimensions_ = set(['level','latitude','longitude'])
    
    def __init__(self,*args,**kargs):
        super(XSection,self).__init__(*args,**kargs)
        self.checkLanguage(self)
        if not 'contour' in self:   
            self['contour'] = [ContourFill()]
        self.plot()

    def plot(self):
        plotter = SlicePlotter(layout = self['layout'],interactive = self['interactive'])
        fields = self['fields']
        if isinstance(fields,Retrieve):
            fields = list(fields.values())
        for field in fields:
            dimensions = field.multipleDimensions()
            if len(dimensions) > 2:
                raise ValueError('Cross-section plotting only deals with 2D fields')
            plotter(field,*self['contour'],x = field.get(dimensions[0]), y= field.get(dimensions[1]))
        if self['interactive']:
            plotter.draw()
        else:
            #name = substitute_variables(self['output_file'],field.metadata())
            plotter.draw(self['output_file'])

xsection = XSection
