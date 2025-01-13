import sys
from semperpy.directive.help import Help
import semperpy.directive.sphinxformatter
from gmaopy.modules.help import *

if len(sys.argv) < 2:
    raise SystemError('need the name of a directive')

directive = sys.argv[1]

h = Help('gmaopy')
text = h(directive,'sphinxformatter')
filename = '%s.txt' % directive
f = open(filename,'w')
f.write('.. _%s:\n\n%s\n' % (directive,text))
f.close()
print(directive)
