#!/bin/bash

if [ "$1" == "" ] ; then
    echo "usage: bash measure1m.sh SLEEP_TIME"
    echo ""
    echo -e "SLEEP_TIME\tsleep for SLEEP_TIME seconds before measuring"
    exit 0
fi

SLEEP_TIME="$1"

sleep "$SLEEP_TIME"

for i in {1..46}
do
    nohup top -bcn 1 -u $USER | head -n 5 >> top.txt 2>&1 &
    nohup iftop -ts 60 | tail -n 8 >> iftop.txt 2>&1 &
    sleep 60
done
