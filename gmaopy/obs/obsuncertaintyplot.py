from semperpy.language.validate import languageValidation
from gmaopy.obs.odsplot import ODSPlot

class ObsUncertaintyPlot(ODSPlot):

    def draw(self,layout,subplot):
        self.dispatchGraphicsAttributes('sym')
        minimum = None
        maximum = None
        for curve in self.curves_:
            data = curve.data
            f = data.variables(variable='obs') - data.variables(variable='omf')
            if f.shape[0] > 0:
                a = data.variables(variable='obs') - data.variables(variable='oma')
                t = data.variables(variable='time')
                t -= 180
                o = data.variables(variable='obs')
                g = data.variables(variable='oma') / (f - a)
                m = g.min()
                if minimum is None or m < minimum:
                    minimum = m
                m = g.max()
                if max is None or m > maximum:
                    maximum = m
                print(curve['graphics']['color'])
                subplot.scatter(t,g,c=curve['graphics']['color'],**self['symbol'])
        if abs(minimum) > abs(maximum):
            maximum = -minimum
        else:
            minimum = -maximum
        if not 'min' in self['xaxis']:
            self['xaxis']['min'] = -180
        if not 'max' in self['xaxis']:
            self['xaxis']['max'] = 180
        self['xaxis'](layout,subplot)
        if not 'min' in self['yaxis']:
            self['yaxis']['min'] = minimum
        if not 'max' in self['yaxis']:
            self['yaxis']['max'] = maximum
        self['yaxis'](layout,subplot)

obsuncertaintyplot = ObsUncertaintyPlot
