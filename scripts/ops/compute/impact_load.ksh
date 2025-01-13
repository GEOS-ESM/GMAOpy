#!/bin/ksh

cat > exec.py << EOF
from gmaopy.modules.obsload import *

textloader(
    files = '${py_store}',
    database = '${py_database}',
    overwrite = '${py_overwrite}'
)
EOF
