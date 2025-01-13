#!/bin/ksh

set -x

python -mcompileall .
python -O -mcompileall .
