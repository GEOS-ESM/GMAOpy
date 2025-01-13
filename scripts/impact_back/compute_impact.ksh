#!/bin/ksh

set -eau

if [[ $# -lt 1 ]]; then
    echo "this script expects one argument: the full path to where ODS impact files have been copied to"
    exit 1
fi
path=$1

install_root=/discover/nobackup/projects/gmao/share/dasilva/lib/python/gmaopy
. $install_root/gmaopy.source

trap 'if [[ -d $root.run ]]; then; mv $root.run $root.ready; fi; exit 1' INT BUS SEGV TERM USR1 USR2


while true; do
    set +e
    all=$(ls -d $path/*.ready)
    error=$?
    set -e
    if [[ $error -ne 0 ]];then
        sleep 60
    else
        set $all
        one=$1
        root=$(basename $one .ready)
        mv $one $root.run
        set +e
        echo "<compute> starting $root.run"
        python compute.py $(basename $root.run) $path
        error=$?
        next=done
        if [[ $error -ne 0 ]];then
            next=ready
            echo "<compute> job failed: $root.run"
        else
            echo "<compute> job success: $root.run"
        fi
        mv $root.run $root.$next
    fi
done
