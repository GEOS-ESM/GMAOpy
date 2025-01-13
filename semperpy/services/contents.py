#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2010
#
# Claude Gibert, April 2010, dev@synopticview.com
#-------------------------------------------------------------------
from semperpy.core.spjson import JSon
from semperpy.services.errors import BadRequest

class Contents(JSon):

    @classmethod
    def decode(self,string):
        try:
            return JSon.decode(string)
        except:
            raise BadRequest("Bad contents ('%s',%s)" % (string,type(string)))
