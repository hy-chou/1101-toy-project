#!/bin/bash

if [ $# != 1 ] ; then
    echo    "NAME"
    echo -e "\tbookiftop.sh - schedule iftop with cron"
    echo
    echo    "DIRECTIONS"
    echo -e "\tWrite the following lines to /etc/cron.d/bookiftop"
    echo
    echo -e "\t\tSHELL=/bin/sh"
    echo -e "\t\tPATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin"
    echo -e "\t\tDIR_B=$(cd ../books && pwd)"
    echo -e "\t\tDIR_C=$(cd .. && pwd)"
    echo -e "\t\t*  *  *  *  * root bash \${DIR_B}/bookiftop.sh \${DIR_C}/try2037_30k 1 30000"
    echo
    echo    "ARGUMENTS"
    echo -e "\tDIR\tabsolute path to the directory to store the data"
    echo -e "\t   \te.g. $HOME/try2035_30k"

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
