#/bin/ksh

set -eau

cat > gen.py << EOF
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
print directive
EOF

target=directives.txt
rm -f $target
cat > $target << \EOF
:mod:`directives` --- Application directives
============================================

.. module:: directives

.. moduleauthor:: Claude Gibert <claude.gibert@synopticview.co.uk>

Contents
********

.. toctree::
   :maxdepth: 1

   
EOF

directives=$(spy_doc directives)
for directive in $directives; do
    echo $directive
    name=$(python gen.py $directive)
    echo "   $name" >> $target
done
