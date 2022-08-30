#!/bin/bash

if [ $# != 1 ] ; then
    FILENAME="booktop.sh"

    echo "NAME"
    echo -e "\t${FILENAME} - schedule top with crontab"
    echo ""
    echo "DIRECTIONS"
    echo -e "\t1. $ crontab -e"
    echo -e "\t2. append the following line:"
    echo -e "\t   * * * * * bash ~/.../${FILENAME} DIR"
    echo ""
    echo "ARGUMENTS"
    echo -e "\tDIR \tabsolute path to the directory to store the data"
    echo -e "\t    \te.g. $HOME/try2035_30k"

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
