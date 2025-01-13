#!/bin/ksh

set -eau

function usage {
    echo "usage: impact_plot.ksh [-o type_of_plot] [-i interval_of_time] date expver [database_name]"
    echo "   -o: specifies the type of plot, to date:"
    echo "       * summary (default)"
    echo "       * timeseries"
    echo "       * channels"
    echo "   -w: specifies which set of data to plot:"
    echo "       * all, all observing systems (default)"
    echo "       * rad, only radiances"
    echo "   -i: specifies the interval of time, to date:"
    echo "       * month (default)"
    echo "       * three_month"
    echo "       * year"
    echo "  date: is the date of the run including time: yyyymmddhh"
    echo "  expver: is the experiment id"
    echo "  database_name (optional): name of the database to use, default 'ops'"
    echo ""
    exit 1
}

# defaults
#--------------------------
script=summary
option=all
interval=month
database_name=ops

while getopts o:i:w: var 
do
    case $var in
        i) interval=$OPTARG;;
        o) script=$OPTARG;;
        w) option=$OPTARG;;
        *) usage;;
    esac
done
shift $OPTIND-1

# checks that the interval given and the script are known
#--------------------------------------------------------
python validate.py time $interval
python validate.py scripts $script $option

if [[ $# -lt 2 ]]; then
    usage
fi
date=$1
expver=$2
if [[ $# -gt 2 ]]; then
    database_name=$3
fi

# load gmaopy
#--------------------------
root=/discover/nobackup/projects/gmao/share/gmao_ops/lib/python/gmaopy
export GMAOPY_VERSION=ops
. $root/gmaopy.source

# update the file containing expid and dates
#--------------------------------------------
python dates.py $date > tmp.$$
mv -f tmp.$$ dates.def

# execute
#--------------------------
python $script.py $date $expver $interval $database_name $option
echo "$interval $script $option job successfully completed"
