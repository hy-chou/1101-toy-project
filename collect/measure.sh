#!/bin/bash

if [ "$2" == "" ] ; then
    echo "usage:  "
    echo "1. sudo su"
    echo "2. nohup bash ../measure.sh SLEEP_TIME END_HOUR > /dev/null 2>&1 &"
    echo ""
    echo -e "SLEEP_TIME\tstart measuring after SLEEP_TIME, eg. 31m"
    echo -e "END_HOUR\tstop measuring at END_HOUR, eg. 2022-08-26T23"
    exit 0
fi

sleep "$1"

mkdir -p txts
mkdir -p txts/tops
mkdir -p txts/iftops

while [ $(date --iso-8601="seconds" | cut -d : -f 1) != "$2" ]
do
    TS=$(date --iso-8601="seconds")
    TS2H=$(echo ${TS} | cut -d : -f 1)

    echo ${TS} >> txts/tops/${TS2H}top.txt
    top -bn 1 | head -n 5 >> txts/tops/${TS2H}top.txt

    echo ${TS} >> txts/iftops/${TS2H}iftop.txt
    iftop -ts 30 | tail -n 4 | head -n 2 >> txts/iftops/${TS2H}iftop.txt
done
