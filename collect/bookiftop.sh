#!/bin/bash

if [ $# != 1 ] ; then
    FILENAME="bookiftop.sh"

    echo "NAME"
    echo -e "\t${FILENAME} - schedule iftop with crontab"
    echo ""
    echo "DIRECTIONS"
    echo -e "\t1. $ sudo crontab -e"
    echo -e "\t2. append the following line:"
    echo -e "\t   * * * * * bash /.../${FILENAME} DIR"
    echo ""
    echo "ARGUMENTS"
    echo -e "\tDIR \tabsolute path to the directory to store the data"
    echo -e "\t    \te.g. $HOME/try2035_30k"

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
