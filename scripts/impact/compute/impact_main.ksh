#!/bin/ksh

set -eaux

function usage {
    echo "usage impact_main [-f] [-o mode] date1 date2 dateincr expver source [path_to_ods_files]"
    echo "   -f: force the writing, overwrite data in the database or overwrite the file"
    echo "   -o mode: function required from the script"
    echo "   where mode is:"
    echo "      - txt: store statistics in text file (default)"
    echo "      - db: store results in the standard storage (database)"
    echo "      - t2db: load statistics from text file to standard storage (database)"
    echo "   and:"
    echo "      date1: first date in interval:"
    echo "      date2: last date in interval:"
    echo "      dateincr: date increment cannot be 0"
    echo "      expver: experiment version"
    echo "      source: oper, odas, aer or exp"
    echo "      path_to_ods_files: full path to where impact ODS files are store (default ./)"
    echo ""
    exit 1
}

# defaults to -o txt
mode=txt
include=impact_compute
py_storer=filestorer
py_store=stats.txt
# default to no overwrite
py_overwrite=False

while getopts o:f var 
do
    case $var in
        f) py_overwrite=True;;
        o) mode=$OPTARG; case $OPTARG in
               (txt)  ;;
               (db)   include=impact_compute; py_storer=dbstorer; py_store=ops;;
               (t2db) include=impact_load; py_store=stats.txt; py_database=ops;;
               (*)    usage;;
           esac
    esac
done
shift $OPTIND-1

# no arguments are excpected if the mode is t2db
#------------------------------------------------
py_location=None
if [[ $mode != t2db ]]; then
    # we expect at least 5 arguments
    #------------------------------------------
    if [[ $# -lt 5 ]]; then
        usage
    fi

    # now we can assign the arguments to be received
    #-----------------------------------------------
    py_date_begin=$1
    py_date_end=$2
    py_date_incr=$3
    py_expver=$4
    py_source=$5
    py_location=./
    if [[ $# -gt 5 ]]; then
        py_location=$6
    fi
fi

# include the right script
#--------------------------
. ./$include.ksh

# load gmaopy
#--------------------------
root=/discover/nobackup/projects/gmao/share/dasilva/lib/python/gmaopy
export GMAOPY_VERSION=ops
. $root/gmaopy.source

# execute
#--------------------------
python exec.py
echo "job successfully completed"
