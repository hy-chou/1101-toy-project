#!/bin/bash

if [ "$5" == "" ] ; then
    echo "usage:  "
    echo "1. cd TARGET_DIR"
    echo "2. bash ../collector.sh DD H1 Hn C1 Cn"
    echo ""
    echo -e "DD\tdate (local)"
    echo -e "H1\tfirst hour (local)"
    echo -e "Hn\tlast hour (local)"
    echo -e "C1\tfirst count (local)"
    echo -e "Cn\tlast count (local)"
    exit 0
fi

DD="$1"
HH="$2"
Hn="$3"
CMD_INFO="nohup node ../getSomeInfo.js $4 $5"
CMD_IP="nohup node ../getSomeIP.js $4 $5"

while [ ! ${HH} == $((${Hn}+1)) ]
do
    ${CMD_INFO} " 0     0 ${HH} ${DD} * *" "10 ${HH} ${DD} * *" > /dev/null 2>&1 &

    ${CMD_IP} "30  0-19 ${HH} ${DD} * *" "30 ${HH} ${DD} * *" > /dev/null 2>&1 &
    ${CMD_IP} "30 20-39 ${HH} ${DD} * *" "50 ${HH} ${DD} * *" > /dev/null 2>&1 &
    if [ ${HH} != 23 ] ; then
        ${CMD_IP} "30 40-59 ${HH} ${DD} * *" "10 $((${HH}+1)) ${DD} * *" > /dev/null 2>&1 &
        HH="$((${HH}+1))"
    else
        ${CMD_IP} "30 40-59 23 ${DD} * *"    "10 0 $((${DD}+1)) * *" > /dev/null 2>&1 &

        sleep 1
        echo "all done."
        exit 0
    fi
done

sleep 1
echo "all done."
