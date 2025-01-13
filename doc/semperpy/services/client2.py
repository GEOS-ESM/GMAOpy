from semperpy.services.client import Client
from semperpy.language.language import Language
from semperpy.core.spjson import JSon

def reader(name):
    f = open(name + ".json","r")
    s = JSon.decode(f)
    f.close()
    return s

def Choice(directive,keyword,values,*args):
    if not values[0] in args:
        raise ValueError("Only values %s are valid for the %s" % (','.join(args),keyword))
    return values

def DiffValidate(directive,keyword,values,count):
    if directive['operator'] == '-':
        if len(values) != count:
            raise ValueError("Wrong number of values for %s, %d expected" % (keyword,count))
    return values

directive = Language.resolveDirective({'operator': '-', 'arguments': [12,8]},"calculate",reader)
client = Client("http://localhost:8880/calculate")
print(client.execute(directive))
