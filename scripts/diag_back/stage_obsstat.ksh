#!/bin/ksh

set -eau

if [[ $# -lt 2 ]]; then
    echo "this script expects two arguments:"
    echo "     - the full path to where ODS impact files should be copied to"
    echo "     - the full path to the file.def describing dates and experiment versions"
    exit 1
fi
path=$1
file=$2

python stage.py $path $file
