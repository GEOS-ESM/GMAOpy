from semperpy.core.date import Date
from semperpy.verify.fielddescriptor import FieldDescriptor

class Forecast(FieldDescriptor):
    
    def adjustValues(self,owner):
        dates = []
        steps = []
        valid = []
        for date in self['date']:
            for step in self['step']:
                dates.append(date)
                steps.append(step)
                v = Date(date) + step
                valid.append(v.intvalue())
        self['date'] = dates
        self['step'] = steps
        self.valid = valid

forecast = Forecast
