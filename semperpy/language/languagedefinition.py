#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, May 2010, claude.gibert@synopticview.com
#-------------------------------------------------------------------
from semperpy.core.tools import to_list

def untouched(value):
    return value

class LanguageDefinition(object):

    @staticmethod
    def directive():
        return {
            "required": [
                "directive",
                "keywords"
            ],
            "valid": {
                "directive"         :    str,
                "keywords"          :    untouched,
                "inherit_from"      :    to_list,
                "specialize_from"   :    untouched,
                "post_validate"     :    to_list,
                "help"              :    to_list,
                "doc"               :    bool
            },
        }

    @staticmethod
    def keywords():
        return {
            "required": [
            ],
            "defaults": {
                "optional":             False,
                "unique":               False,
                "remove":               False,
                "lowercase":            True,
                "type":                 "",
                "ignore_type_errors":   False,
                "distribute_type":      True,
                "validate":             []
            },
            "valid": {
                "optional":             bool,
                "unique":               bool,
                "remove":               bool,
                "type":                 untouched,
                "ignore_type_errors":   bool,
                "distribute_type":      bool,
                "default_value":        untouched,
                "alias":                to_list,
                "validate":             to_list,
                "lowercase":            bool,
                "help":                 to_list,
            }
        }
