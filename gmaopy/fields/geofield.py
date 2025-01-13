from semperpy.directive.directive import Directive

class GeoField(Directive):

    def __init__(self,*args,**kwargs):
        super(GeoField,self).__init__(*args,**kwargs)
        self.checkLanguage()

geofield = GeoField

class Analysis(GeoField):
    pass

analysis = Analysis


class Forecast(GeoField):
    pass

forecast = Forecast
