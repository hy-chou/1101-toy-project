#!/bin/bash

DIR_N="/etc/openvpn/nordvpn"


if [ $# -lt 3 ] ; then
    echo -e "
SYNOPSIS
    bash series-novpn.sh PATH/TO/KUKUDY PATH/TO/TARGET_DIR CHANNEL_COUNT
    OR write the following to /etc/cron.d/kukudy

DIR_K=$(pwd)

32 18 06 11 * $USER bash \${DIR_K}/scripts/series-novpn.sh \${DIR_K} \${DIR_K}/k9999_100_25Hz 100
"
    exit 1
fi


DIR_K=$1
TARGET_DIR=$2
CHANNEL_COUNT=$3


mkdir -p ${TARGET_DIR}/logs
cd ${TARGET_DIR}

echo -en "$(date -uIns)\t#START\n" >> ${TARGET_DIR}/logs/checkpoint.txt

echo -en "$(cat ../.env)\n"        >> ${TARGET_DIR}/logs/checkpoint.txt

/usr/bin/node ../updateStreams.js ${CHANNEL_COUNT}
echo -en "$(date -uIns)\tuS done\n" >> ${TARGET_DIR}/logs/checkpoint.txt

for ROUND in {0..19}
do
    /usr/bin/node ../updateEdges.js
    echo -en "$(date -uIns)\tuE$ROUND done\n" >> ${TARGET_DIR}/logs/checkpoint.txt

    sleep 30s

    /usr/bin/node ../updateEdges.js
    echo -en "$(date -uIns)\tuE$ROUND done\n" >> ${TARGET_DIR}/logs/checkpoint.txt

    sleep 30s
done

echo -en "$(date -uIns)\t#DONE\n" >> ${TARGET_DIR}/logs/checkpoint.txt

exit 0
