from semperpy.core.spjson import JSon
from .deftypes import DefTypes

class Language(DefTypes):

    def __str__(self):
        defaults = {
            'int': 0,
            'bool': False,
            'float': 0.0,
            'str': 'na'
        }
        keys = list(self.types_.keys())
        keys.sort()
        lang = dict(
            directive = 'obrecord',
            keywords = {
            }
        )
        for key in keys:
            t = self.types_[key]
            d = dict(
                unique = True,
                optional = True,
                type = t,
                default_value = defaults[t]
            )
            lang['keywords'][key] = d
        return JSon.encode(**lang)
