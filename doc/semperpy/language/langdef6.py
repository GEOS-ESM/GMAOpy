from semperpy.language.language import Language
from semperpy.core.spjson import JSon

def ValidateChoice(directive,keyword,values,*args):
    for value in values:
        if not value in args:
                raise ValueError("for keyword %s. The value: '%s' is not in the set: %s" % (keyword, value, ', '.join([str(x) for x in args])))
    return values

def reader(name):
    f = open(name + ".json","r") # a configuration path could be used
    s = JSon.decode(f)
    f.close()
    return s

directive = dict(
    date = 2020101012,
    step = [24,48],
    param = "geopotential",
    level = [500,1000],
    experiment_version = "0012",
)
print(Language.resolveDirective(directive, "retrieve", reader))
