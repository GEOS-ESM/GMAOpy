from semperpy.language.language import Language

#-----------------------------------------------------------
# The language
#-----------------------------------------------------------
retrieve = dict(
    directive = "retrieve",
    keywords = dict(
        date = dict(
        ),
        step = dict(
        ),
        parameter = dict(
        ),
        level = dict(
        ),
        experiment_version = dict(
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
    experiment_version = ["0012","0013"],
)
print(Language.resolveDirective(directive, "retrieve", reader))
