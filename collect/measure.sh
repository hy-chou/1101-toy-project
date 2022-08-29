#!/bin/bash

if [ "$1" == "" ] ; then
    echo "usage:  "
    echo "1. sudo su"
    echo "2. nohup bash ../measure.sh END_MIN > /dev/null 2>&1 &"
    echo ""
    echo -e "END_MIN \tstop measuring at END_MIN (local time), eg. 2022-08-27T17:58"
    exit 0
fi

mkdir -p txts/tops txts/iftops

while [ $(date --iso-8601="minutes" | head -c ${#1}) != "$1" ]
do
    TS=$(date -u --iso-8601="seconds")
    TS2H=$(echo ${TS} | cut -d : -f 1)

    echo ${TS} >> txts/tops/${TS2H}top.txt
    top -bn 1 | head -n 5 >> txts/tops/${TS2H}top.txt

    echo ${TS} >> txts/iftops/${TS2H}iftop.txt
    iftop -ts 30 | tail -n 4 | head -n 2 >> txts/iftops/${TS2H}iftop.txt
done
