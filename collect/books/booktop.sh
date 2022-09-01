#!/bin/bash

if [ $# != 1 ] ; then
    FILENAME="booktop.sh"

    echo    "NAME"
    echo -e "\t${FILENAME} - schedule top with cron"
    echo
    echo    "DIRECTIONS"
    echo -e "\tWrite the following lines to /etc/cron.d/booktop"
    echo
    echo -e "\t\tSHELL=/bin/sh"
    echo -e "\t\tPATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin"
    echo -e "\t\tDIR_B=$(cd ../books && pwd)"
    echo -e "\t\tDIR_C=$(cd .. && pwd)"
    echo -e "\t\t*  *  *  *  * $USER bash \${DIR_B}/booktop.sh \${DIR_C}/try2037_30k 1 30000"
    echo
    echo    "ARGUMENTS"
    echo -e "\tDIR\tabsolute path to the directory to store the data"
    echo -e "\t   \te.g. $HOME/try2035_30k"

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
