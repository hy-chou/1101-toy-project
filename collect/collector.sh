#!/bin/bash

if [ "$5" == "" ] ; then
    echo "usage:  "
    echo "1. cd TARGET_DIR"
    echo "2. bash ../collector.sh DD H1 Hn P1 Pn"
    echo ""
    echo -e "DD\tdate (local)"
    echo -e "H1\tfirst hour (local)"
    echo -e "Hn\tlast hour (local)"
    echo -e "P1\tstart from the P1-th channel"
    echo -e "Pn\tto the Pn-th channel"
    exit 0
fi

DD="$1"
HH="$2"
Hn="$3"
CMD_STRM="nohup node ../getActiveStreams.js $4 $5"
CMD_EDGE="nohup node ../getActiveEdges.js   $4 $5"

while [ ! ${HH} == $((${Hn}+1)) ]
do
    ${CMD_STRM} "    0 ${HH} ${DD} * *" " 1 ${HH} ${DD} * *" > /dev/null 2>&1 &

    ${CMD_EDGE} " 0-19 ${HH} ${DD} * *" "30 ${HH} ${DD} * *" > /dev/null 2>&1 &
    ${CMD_EDGE} "20-39 ${HH} ${DD} * *" "50 ${HH} ${DD} * *" > /dev/null 2>&1 &
    if [ ${HH} != 23 ] ; then
        ${CMD_EDGE} "40-59 ${HH} ${DD} * *" "10 $((${HH}+1)) ${DD} * *" > /dev/null 2>&1 &
        HH="$((${HH}+1))"
    else
        ${CMD_EDGE} "40-59 23 ${DD} * *"    "10 0 $((${DD}+1)) * *" > /dev/null 2>&1 &

        sleep 1
        echo "all done."
        exit 0
    fi
done

sleep 1
echo "all done."
