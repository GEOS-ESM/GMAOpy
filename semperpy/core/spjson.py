#----------------------------------------------------------------------------
# SemperPy Copyright SynopticView, GMAO 2009-2010
#
# Claude Gibert, April 2010, dev@synopticview.com
#-------------------------------------------------------------------
try:
    import json as js
except ImportError:
    import simplejson as js
    # Documented in http://tinyurl.com/ykhqrre, thanks to Carlos Valiente
    js.encoder.c_make_encoder = None
import types
from io import IOBase

# Documented in http://tinyurl.com/ykhqrre, thanks to Carlos Valiente
js.encoder.FLOAT_REPR = lambda f: ("%g" % f)

class JSon(object):

    @classmethod
    def encode(self,file = None, **kargs):
        if file:
            return js.dump(file,kargs)
        else:
            return js.dumps(kargs)

    @classmethod
    def decode(self,string):
#        def no_unicode(d):
        # this can be removed in python 3.0
        # we convert unicode string to standard python ascii string
        # this is because unicode strings cannot be used as variable
        # names in python eallier than 3.0. If we decode a dictionary
        # **myarg is invalid.
#	     if isinstance(d,dict):
#		 return dict([(str(k),no_unicode(v)) for k,v in d.items()])
#	     elif isinstance(d,list):
#		 return [ no_unicode(x) for x in d ]
#	     elif type(d) == str:
#		 return str(d)
#	     else:
#		 return d
#
#	 if type(string) == types.FileType:
         try:
             getattr(string,'name','<unknown>')
             return js.load(string)#,object_hook=no_unicode)
         except:
             return js.loads(string)#,object_hook=no_unicode)
