from semperpy.language.language import Language

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
