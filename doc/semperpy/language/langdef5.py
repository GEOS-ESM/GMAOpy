from semperpy.core.tools import dictionary
from semperpy.language.language import Language

field_directive = dict(
    directive = "field",
    specialize_from = {
        "source == 'merra'": "merra",
        "parameter == 'mslp' or parameter == 't2m'" : "surface"
    },
    keywords = dict(
        source = dict(
            type = str,
        ),
        type = dict(
            type = str,
            optional = True,
            default_value = "fc" # forecast
        ),
        level = dict(
            type = int,
            optional = True,
            default_value = 500, # 500 hPa
        ),
        leveltype = dict(
            type = str,
            optional = True,
            default_value = "pl" # pressure level
        ),
        parameter = dict(
            type = str,
        )
    )
)

surface_directive = dict(
    directive = "surface",
    keywords = dict(
        level = dict(
            remove = True
        ),
        leveltype = dict(
            type = str,
            optional = True,
            default_value = "sfc" # surface level
        ),
    )
)

merra_directive = dict(
    directive = "merra",
    keywords = dict(
        type = dict(
            type = str,
            optional = True,
            default_value = "an" # analysis
        ),
        dataset = dict(
            type = str
        )
    )
)

def reader(s):
    dirs = dict(
        field   = field_directive,
        surface = surface_directive,
        merra   = merra_directive,
    )
    return dirs[s]

directive = dict(
    source = 'oper',
    parameter = 't2m',
)
print(dictionary(Language.resolveDirective(directive, "field", reader)))
