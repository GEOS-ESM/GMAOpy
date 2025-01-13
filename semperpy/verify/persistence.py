from semperpy.verify import FieldDescriptor

class Persistence(FieldDescriptor):
    
    def adjustValues(self,owner):
        fc = owner['forecast']
        self.inherit_from(owner['reference'])
        self['date'] = fc['date']
        self['step'] = [0] * len(fc['step'])

persistence = Persistence
