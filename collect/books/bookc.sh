#!/bin/bash

if [ $# != 3 ] ; then
    echo -en "
NAME
  \tbookc.sh - schedule the probes with cron

ARGUMENTS
  \tDIR\tabsolute path to the directory to store the data
  \t   \te.g. $HOME/try2040_30k

  \tC1 \tstart from the C1-th channel
  \t   \te.g. 1

  \tCN \tto the CN-th channel
  \t   \te.g. 30000

DIRECTIONS
  \tWrite the following lines to /etc/cron.d/bookc

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

DIR_C=$(cd .. && pwd)

59  *  *  *  * $USER bash \${DIR_C}/books/bookc.sh \${DIR_C}/try2040_30k 1 30000
"
    exit 0
fi

TS9=$(TZ='Asia/Tokyo' date -Iseconds)
TS10=$(TZ='Asia/Vladivostok' date -Iseconds)
H9=$(echo ${TS9} | cut -d T -f 2 | cut -d : -f 1)
H10=$(echo ${TS10} | cut -d T -f 2 | cut -d : -f 1)

mkdir -p $1 && cd $1

CMD_STRM="nohup node ../getActiveStreams.js $2 $3"
CMD_EDGE="nohup node ../getActiveEdges.js   $2 $3"

${CMD_STRM} "    5 ${H9} * * *" > /dev/null 2>&1 &
${CMD_STRM} "   15 ${H9} * * *" > /dev/null 2>&1 &
${CMD_STRM} "   25 ${H9} * * *" > /dev/null 2>&1 &
${CMD_STRM} "   35 ${H9} * * *" > /dev/null 2>&1 &
${CMD_STRM} "   45 ${H9} * * *" > /dev/null 2>&1 &
${CMD_STRM} "   55 ${H9} * * *" > /dev/null 2>&1 &

${CMD_EDGE} " 0-19 ${H9} * * *" > /dev/null 2>&1 &
${CMD_EDGE} "20-39 ${H9} * * *" > /dev/null 2>&1 &
${CMD_EDGE} "40-59 ${H9} * * *" > /dev/null 2>&1 &
