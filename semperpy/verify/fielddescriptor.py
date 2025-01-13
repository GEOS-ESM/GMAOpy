import copy
from semperpy.directive import Directive
from gmaopy.directives.retrieve import Retrieve

class FieldDescriptor(Directive):

    def retrieveData(self,args):
        ret = copy.copy(self)
        ret['date'] = list(set(ret['date']))
        ret['step'] = list(set(ret['step']))
        p = Retrieve(
            variables = args,
            fields = ret,
            trydap = False,
        )
        return list(p.values())

field=FieldDescriptor
