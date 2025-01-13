from semperpy.language.validate import languageValidation
from gmaopy.obs.odsplot import ODSPlot

class ScatterPlot(ODSPlot):

    def draw(self,layout,subplot):
        self.dispatchGraphicsAttributes('sym')
        subplot.axhline(linestyle = ':', color = 'black')
        subplot.axvline(linestyle = ':', color = 'black')
        horizontal = self.curves_[0].data.variables(variable=self.data['variable'][0])
        vertical = self.curves_[0].data.variables(variable=self.data['variable'][1])
        subplot.scatter(horizontal,vertical,c=self.curves_[0]['graphics']['color'],**self['symbol'])
        if not 'min' in self['xaxis']:
            min, max = self.setMinMax(subplot,self['xaxis'])
            self['xaxis'](layout,subplot,min = min, max = max)
        else:
            self['xaxis'](layout,subplot)
        if not 'min' in self['yaxis']:
            min, max = self.setMinMax(subplot,self['yaxis'])
            self['yaxis'](layout,subplot,min = min, max = max)
        else:
            self['yaxis'](layout,subplot)

    def setMinMax(self,subplot,axis):
        min,max = axis.minmax(subplot)
        if abs(min) > abs(max):
            max = -min
        else:
            min = -max
        return min, max

scatterplot = ScatterPlot
