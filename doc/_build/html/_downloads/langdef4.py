from semperpy.language.language import Language

parameter = dict(
    directive = "parameter",
    keywords = dict(
        parameter = dict(
        ),
        level = dict(
            type = int,
            default_value = 500,
            optional = True,
        ),
    )
)

date = dict(
    directive = "date",
    keywords = dict(
        date = dict(
            type = int,
        ),
        step = dict(
            type = int,
        ),
        level = dict(
            type = str,
        )
    )
)

retrieve = dict(
    directive = "retrieve",
    inherit_from = ["parameter","date"],
    keywords = dict(
        experiment_version = dict(
            unique = True,
            alias = "expver"
        ),
        target = dict(
        )
    )
)

def reader(s):
    dirs = dict(
        parameter = parameter,
        date = date,
        retrieve = retrieve
    )
    return dirs[s]

directive = dict(
    date = 2020101012,
    step = [24,48],
    parameter = "geopotential",
    level = [500,1000],
    experiment_version = "0012",
    target = "myFile"
)
print(Language.resolveDirective(directive, "retrieve", reader))
