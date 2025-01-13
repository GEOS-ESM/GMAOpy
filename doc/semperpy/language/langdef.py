from semperpy.language.language import Language

#-----------------------------------------------------------
# These are validators written here for the example
#-----------------------------------------------------------
# value is always passed as a list
def ValidateChoice(directive,keyword,values,*args):
    for value in values:
        if not value in args:
            raise ValueError("for keyword %s. The value: '%s' is not in the set: %s" % (keyword, value, ', '.join(args)))
    return values

# value is always passed as a list
def ValidateRange(directive,keyword,values,min,max):
    for value in values:
        if value < min or value > max:
            raise ValueError("for keyword %s. The value: '%s' is not in the interval: [%d,%d]" % (keyword, value, min, max))
    return values

#-----------------------------------------------------------
# The language
#-----------------------------------------------------------
retrieve = dict(
    directive = "retrieve",
    keywords = dict(
        date = dict(
            type = int,
        ),
        step = dict(
            type = int,
            validate  = [ValidateRange,0,168],
        ),
        parameter = dict(
            # types and validators can be passed litterally or just their name
            validate = ["ValidateChoice","geopotential","temperature"],
            alias = "param",
        ),
        level = dict(
            type = int,
            default_value = 500,
            optional = True,
        ),
        experiment_version = dict(
            unique = True
        )
    )
)

def reader(s):
    return retrieve

#-----------------------------------------------------------
# Testing the example
#-----------------------------------------------------------
directive = dict(
    date = 2020101012,
    step = [24,48],
    param = "geopotential",
    level = [500,1000],
    experiment_version = "0012",
)
print(Language.resolveDirective(directive, "retrieve", reader))
directive = dict(
    date = 2020101012,
    step = [24,48,240],
    param = "windspeed",
    level = [500,1000],
    experiment_version = "0012",
)
try:
    print(Language.resolveDirective(directive, "retrieve", reader))
    print()
except Exception as e:
    print(e)
directive = dict(
    date = 2020101012,
    param = "geopotential",
    Level = [500,1000],
    experiment_version = ["0012","0013"]
)
try:
    print(Language.resolveDirective(directive, "retrieve", reader))
    print()
except Exception as e:
    print(e)
