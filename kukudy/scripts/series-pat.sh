#!/bin/bash

DIR_N="/etc/openvpn/nordvpn"


if [ $# -lt 4 ] ; then
    echo -e "
SYNOPSIS
    sudo bash series.sh PATH/TO/KUKUDY PATH/TO/TARGET_DIR CHANNEL_COUNT COUNTRY_CODES
    OR write the following to /etc/cron.d/kukudy

DIR_K=$(pwd)

25 21 25 10 * root bash \${DIR_K}/scripts/series.sh \${DIR_K} \${DIR_K}/k5018_200_USUKCAFRDE 200 US UK CA FR DE
"
    exit 1
fi

DIR_K=$1
TARGET_DIR=$2
CHANNEL_COUNT=$3
shift
shift
shift
COUNTRY_CODES=$@


mkdir -p ${TARGET_DIR}/logs
cd ${TARGET_DIR}

for CCODE in ${COUNTRY_CODES}
do
    echo -en "$(date -uIns)\t$CCODE\n" >> ${TARGET_DIR}/logs/checkpoint.txt

    SERVER_ID="$(/usr/bin/node ${DIR_K}/utils/getServersRecommendations.js $CCODE)"
    if [ $? == 1 ] ; then
        exit 1
    fi
    echo -en "$(date -uIns)\t${SERVER_ID}\n" >> ${TARGET_DIR}/logs/checkpoint.txt
    CONF="${SERVER_ID}.nordvpn.com.udp.ovpn"

    /usr/sbin/openvpn                                  \
        --config         ${DIR_N}/ovpn_udp/${CONF}     \
        --auth-user-pass ${DIR_N}/auth.txt             \
        --writepid       ${DIR_N}/logs/pid.txt         \
        --log-append     ${TARGET_DIR}/logs/$(date -uI).log  \
        --daemon

    /usr/bin/node ../utils/waitForVPN.js
    echo -en "$(date -uIns)\t${SERVER_ID} connected\n" >> ${TARGET_DIR}/logs/checkpoint.txt

    /usr/bin/node ../updateStreams.js ${CHANNEL_COUNT}
    echo -en "$(date -uIns)\tuS done\n" >> ${TARGET_DIR}/logs/checkpoint.txt
    /usr/bin/node ../getPATs.js
    echo -en "$(date -uIns)\tgetPATs done\n" >> ${TARGET_DIR}/logs/checkpoint.txt

    kill -15 $(cat ${DIR_N}/logs/pid.txt)
    echo -en "$(date -uIns)\t${SERVER_ID} killed\n" >> ${TARGET_DIR}/logs/checkpoint.txt

    sleep 1m
done

echo -en "$(date -uIns)\t#DONE\n" >> ${TARGET_DIR}/logs/checkpoint.txt

exit 0
