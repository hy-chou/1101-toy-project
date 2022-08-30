#!/bin/bash

if [ $# != 3 ] ; then
    echo "NAME"
    echo -e "\tbookc.sh - schedule the probes with crontab"
    echo ""
    echo "DIRECTIONS"
    echo -e "\t1. $ crontab -e"
    echo -e "\t2. append the following line:"
    echo -e "\t   59 * * * * bash ~/.../bookc.sh DIR C1 CN"
    echo ""
    echo "ARGUMENTS"
    echo -e "\tDIR \tabsolute path to the directory to store the data"
    echo -e "\t    \te.g. ~/try2035_30k"
    echo ""
    echo -e "\tC1  \tstart from the C1-th channel"
    echo -e "\t    \te.g. 1"
    echo ""
    echo -e "\tCN  \tto the CN-th channel"
    echo -e "\t    \te.g. 30000"

    exit 0
fi

TS9=$(TZ='Asia/Tokyo' date -Iseconds)
TS10=$(TZ='Asia/Vladivostok' date -Iseconds)
H9=$(echo ${TS9} | cut -d T -f 2 | cut -d : -f 1)
H10=$(echo ${TS10} | cut -d T -f 2 | cut -d : -f 1)

mkdir -p $1 && cd $1

CMD_STRM="nohup node ../getActiveStreams.js $2 $3"
CMD_EDGE="nohup node ../getActiveEdges.js   $2 $3"

${CMD_STRM} "    0 ${H9} * * *" " 6 ${H9} * * *" > /dev/null 2>&1 &
${CMD_STRM} "   12 ${H9} * * *" "18 ${H9} * * *" > /dev/null 2>&1 &
${CMD_STRM} "   24 ${H9} * * *" "30 ${H9} * * *" > /dev/null 2>&1 &
${CMD_STRM} "   36 ${H9} * * *" "42 ${H9} * * *" > /dev/null 2>&1 &
${CMD_STRM} "   48 ${H9} * * *" "54 ${H9} * * *" > /dev/null 2>&1 &

${CMD_EDGE} " 0-19 ${H9} * * *" "30 ${H9} * * *" > /dev/null 2>&1 &
${CMD_EDGE} "20-39 ${H9} * * *" "50 ${H9} * * *" > /dev/null 2>&1 &
${CMD_EDGE} "40-59 ${H9} * * *" "10 ${H10} * * *" > /dev/null 2>&1 &
