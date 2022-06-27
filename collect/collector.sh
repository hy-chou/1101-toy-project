#!/bin/bash

if [ "$3" == "" ] ; then
    echo "usage:  "
    echo "1. cd TARGET_DIR"
    echo "2. bash ../collector.sh DD H1 Hn"
    echo ""
    echo -e "DD\tdate (local)"
    echo -e "H1\tfirst hour (local)"
    echo -e "Hn\tlast hour (local)"
    exit 0
fi

DD="$1"
HH="$2"
Hn="$3"
CMD_LEFT="nohup node ../scheduler10.js"

while [ ! ${HH} == $((${Hn}+1)) ]
do
    ${CMD_LEFT} "00-19 ${HH} ${DD} * *" "30 ${HH} ${DD} * *" > /dev/null 2>&1 &
    ${CMD_LEFT} "20-39 ${HH} ${DD} * *" "50 ${HH} ${DD} * *" > /dev/null 2>&1 &
    # echo "${CMD_LEFT} \"00-19 ${HH} ${DD} * *\" \"30 ${HH} ${DD} * *\" > /dev/null 2>&1 &"
    # echo "${CMD_LEFT} \"20-39 ${HH} ${DD} * *\" \"50 ${HH} ${DD} * *\" > /dev/null 2>&1 &"
    if [ ${HH} != 23 ] ; then
        ${CMD_LEFT} "40-59 ${HH} ${DD} * *" "10 $((${HH}+1)) ${DD} * *" > /dev/null 2>&1 &
        # echo "${CMD_LEFT} \"40-59 ${HH} ${DD} * *\" \"10 $((${HH}+1)) ${DD} * *\" > /dev/null 2>&1 &"
        HH="$((${HH}+1))"
    else
        ${CMD_LEFT} "40-59 23 ${DD} * *" "10 0 $((${DD}+1)) * *" > /dev/null 2>&1 &
        # echo "${CMD_LEFT} \"40-59 23 ${DD} * *\" \"10 0 $((${DD}+1)) * *\" > /dev/null 2>&1 &"
        exit 0
    fi
done

sleep 1
echo "all done."
