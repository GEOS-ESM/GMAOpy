#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, May 2010, claude.gibert@synopticview.com
#-------------------------------------------------------------------
from semperpy.core.factory import Factory

languageValidation = Factory()
#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2010
#
# Claude Gibert, June 2010, dev@synopticview.com
#-------------------------------------------------------------------
def ValidateChoice(directive,keyword,values,*args):
    for value in values:
        if not value in args:
            raise ValueError("for keyword %s. The value: '%s' is not in the set: %s" % (keyword, value, ', '.join([str(x) for x in args])))
    return values

def CopyKeyword(directive,keyword,values,dest,src,make_default='yes'):
    if not dest in directive:
        directive[dest] = directive[src]
        if make_default == 'yes':
            directive.setDefault(dest)
    return directive

def checkCount(directive,keyword,values,count):
    if len(directive[keyword]) != count:
        raise ValueError("for keyword %s, the number of values expected is %d" % (keyword,count))
    return directive[keyword]

languageValidation.register('ValidateChoice',ValidateChoice)
languageValidation.register('CopyKeyword',CopyKeyword)
languageValidation.register('CheckCount',checkCount)
