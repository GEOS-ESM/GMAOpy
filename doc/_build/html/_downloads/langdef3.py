from semperpy.language.language import Language

#----------------------------------------------------
# This is how we validate the values of steps, see
# how it is parameterised in the language definition
# values is always passed as a list
#----------------------------------------------------
def ValidateChoice(directive,keyword,values,*args):
    for value in values:
        if not value in args:
            raise ValueError("for keyword %s. The value: '%s' is not in the set: %s" % (keyword, value, ', '.join([str(x) for x in args])))
    return values

retrieve = dict(
    directive = "retrieve",
    keywords = dict(
        date = dict(
            # dates will be converted to integer
            type = int,
        ),
        step = dict(
            # steps will be converted to integer
            type = int,
            validate = [ValidateChoice,24,48,72,96,120,144,168]
        ),
        parameter = dict(
        ),
        level = dict(
        ),
        experiment_version = dict(
            # you can now use ev or expver as well as experiment_version
            # but you can only specify one of these
            unique = True,
            alias = ["ev","expver"],
        )
    )
)

def reader(s):
    return retrieve

directive = dict(
    date = 2020101012,
    step = ['24','49'],
    parameter = "geopotential",
    level = [500,1000],
    expver = "0012",
)
print(Language.resolveDirective(directive, "retrieve", reader))
