from semperpy.directive import Directive
from semperpy.core.tools import dictionary, substitute_variables
from semperpy.plot.matplotlib import *
from gmaopy.directives.retrieve import Retrieve

class PlotFields(Directive):
    
    def __init__(self,*args,**kargs):
        super(PlotFields,self).__init__(*args,**kargs)
        self.checkLanguage(self)
        if not 'contour' in self:   
            self['contour'] = ContourFill()
        if not 'geography' in self:   
            self['geography'] = Geography()
        self.plot()

    def plot(self):
        plotter = GeoPlotter(layout = self['layout'],interactive = self['interactive'])
        fields = self['fields']
        if isinstance(fields,Retrieve):
            fields = list(fields.values())
        for field in fields:
            plotter(field,self['geography'],self['contour'])
        if self['interactive']:
            plotter.draw()
        else:
            name = substitute_variables(self['output_file'],field.metadata())
            plotter.draw(name)

geoplot = PlotFields
