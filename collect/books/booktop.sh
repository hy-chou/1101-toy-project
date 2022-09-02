#!/bin/bash

if [ $# != 1 ] ; then
    echo -en "
NAME
  \tbooktop.sh - schedule top with cron

ARGUMENTS
  \tDIR\tabsolute path to the directory to store the data
  \t   \te.g. $HOME/try2038_30k

DIRECTIONS
  \tWrite the following lines to /etc/cron.d/booktop

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

DIR_C=$(cd .. && pwd)

 *  *  *  *  * $USER bash \${DIR_C}/books/booktop.sh \${DIR_C}/try2038_30k
"

    exit 0
fi

TS=$(date -u -Iseconds)
TS2H=$(echo "${TS}" | cut -d : -f 1)

mkdir -p "$1/txts/iftops"
touch "$1/txts/iftops/${TS2H}iftop.txt"

mkdir -p "$1/txts/tops" && cd "$1/txts/tops"

for i in {0..1}
do
    TS=$(date -u -Iseconds)
    TS2H=$(echo "${TS}" | cut -d : -f 1)

    LINES=$(top -bn 1 | head -n 5)

    echo "${TS}" >> ${TS2H}top.txt
    echo "${LINES}" >> ${TS2H}top.txt

    sleep 30s
done
