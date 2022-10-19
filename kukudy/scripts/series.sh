#!/bin/bash

DIR_N="/etc/openvpn/nordvpn"


if [ $# -lt 3 ] ; then
    echo -e "
SYNOPSIS
    sudo bash series.sh PATH/TO/KUKUDY PATH/TO/TARGET_DIR COUNTRY_CODES
    OR write the following to /etc/cron.d/kukudy

DIR_K=$(pwd)

41 01 20 10 * root bash \${DIR_K}/scripts/series.sh \${DIR_K} \${DIR_K}/pg US UK CA FR DE
"
    exit 1
fi

DIR_K=$1
TARGET_DIR=$2
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
    /usr/bin/node ../updateStreams.js
    /usr/bin/node ../updateEdges.js

    kill -15 $(cat ${DIR_N}/logs/pid.txt)

    sleep 3
done

echo -en "$(date -uIns)\t#DONE\n" >> ${TARGET_DIR}/logs/checkpoint.txt

exit 0
