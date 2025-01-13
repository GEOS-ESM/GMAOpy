#!/bin/ksh

set -eau

if [[ $# -ne 2 ]]; then
    echo "usage: date expver where:"
    echo "  - date has the format YYYYMMDDHH"
    echo "  - exvper is a string"
    exit 1
fi

date=$1
expver=$2

./impact_plot.ksh -o summary    -w all -i month $date $expver &
./impact_plot.ksh -o summary    -w all -i three_month $date $expver &
./impact_plot.ksh -o summary    -w all -i year $date $expver &
./impact_plot.ksh -o summary    -w rad -i month $date $expver &
./impact_plot.ksh -o summary    -w rad -i three_month $date $expver &
./impact_plot.ksh -o summary    -w rad -i year $date $expver &

./impact_plot.ksh -o timeseries -w all -i month $date $expver &
./impact_plot.ksh -o timeseries -w all -i three_month $date $expver &
./impact_plot.ksh -o timeseries -w all -i year $date $expver &
./impact_plot.ksh -o timeseries -w rad -i month $date $expver &
./impact_plot.ksh -o timeseries -w rad -i three_month $date $expver &
./impact_plot.ksh -o timeseries -w rad -i year $date $expver &

./impact_plot.ksh -o channels   -w all -i month $date $expver &
./impact_plot.ksh -o channels   -w all -i three_month $date $expver &
./impact_plot.ksh -o channels   -w all -i year $date $expver &
wait
