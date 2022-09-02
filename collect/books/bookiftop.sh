#!/bin/bash

if [ $# != 1 ] ; then
    echo -en "
NAME
  \tbookiftop.sh - schedule iftop with cron

ARGUMENTS
  \tDIR\tabsolute path to the directory to store the data
  \t   \te.g. $HOME/try2038_30k

DIRECTIONS
  \tWrite the following lines to /etc/cron.d/bookiftop

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

DIR_C=$(cd .. && pwd)

 *  *  *  *  * root bash \${DIR_C}/books/bookiftop.sh \${DIR_C}/try2038_30k
"
    exit 0
fi

sleep 10s

mkdir -p "$1/txts/iftops" && cd "$1/txts/iftops"

for i in {0..1}
do
    TS=$(date -u -Iseconds)
    TS2H=$(echo "${TS}" | cut -d : -f 1)

    LINES=$(sudo iftop -t -s 30 -L 99)

    echo "${TS}" >> ${TS2H}iftop.txt
    echo "${LINES}" >> ${TS2H}iftop.txt
done
