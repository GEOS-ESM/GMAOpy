from semperpy.verify import FieldDescriptor

class Analysis(FieldDescriptor):
    
    def adjustValues(self,owner):
        fc = owner['forecast']
        self.inherit_from(fc)
        self['date'] = fc.valid
        self['step'] = [0] * len(fc['step'])

analysis = Analysis
