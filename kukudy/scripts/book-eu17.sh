#!/bin/bash

if [ $# -lt 4 ] ; then
    echo -e "
SYNOPSIS
    sudo bash bookvpn.sh PATH/TO/KUKUDY PATH/TO/TARGET_DIR CHANNEL_COUNT ROUND_COUNT DURATION COUNTRY_CODES
    OR write the following to /etc/cron.d/kukudy

DIR_K=$(pwd)

00 01 07 11 * root bash \${DIR_K}/scripts/bookvpn.sh \${DIR_K} \${DIR_K}/k5065_30k_25Hz_USUKCAFRDE_8R 30000 8 86400 US UK CA FR DE
"
    exit 1
fi

DIR_K=$1
TARGET_DIR=$2
CHANNEL_COUNT=$3
ROUND_COUNT=$4
DURATION=$5
shift
shift
shift
shift
shift


for CITY_NAME in Madrid London Paris Amsterdam Marseille Frankfurt Milan Oslo Copenhagen Berlin Prague Vienna Stockholm Warsaw Helsinki
do
    TARGET_SUBDIR="${TARGET_DIR}_$CITY_NAME"
    mkdir -p ${TARGET_SUBDIR}/logs
    cd ${TARGET_SUBDIR}

    echo -en "$(date -uIns)\t$CITY_NAME\n" >> ${TARGET_SUBDIR}/logs/checkpoint.txt

    SERVER_ID="$(/usr/bin/node ${DIR_K}/utils/getSRByCityForEU17.js $CITY_NAME)"
    if [ $? == 1 ] ; then
        echo -en "$(date -uIns)\t${SERVER_ID}\n" >> ${TARGET_SUBDIR}/logs/checkpoint.txt
        exit 1
    fi
    echo -en "$(date -uIns)\t${SERVER_ID}\n" >> ${TARGET_SUBDIR}/logs/checkpoint.txt
    CONF="${SERVER_ID}.nordvpn.com.udp.ovpn"

    /usr/sbin/openvpn                                           \
        --config         ${DIR_K}/nordvpn/ovpn_udp/${CONF}      \
        --auth-user-pass ${DIR_K}/nordvpn/auth.txt              \
        --writepid       ${DIR_K}/nordvpn/pid.txt               \
        --log-append     ${TARGET_SUBDIR}/logs/$(date -uI).log  \
        --daemon

    /usr/bin/node ../utils/waitForVPN.js
    echo -en "$(date -uIns)\t${SERVER_ID} vpn connected\n" >> ${TARGET_SUBDIR}/logs/checkpoint.txt

    T_START=$(date "+%s")
    for ROUND in $(seq ${ROUND_COUNT})
    do
        T_DIFF=$(($(date "+%s") - ${T_START}))
        echo -en "$(date -uIns)\t${SERVER_ID} ${T_DIFF} / ${DURATION}\n" >> ${TARGET_SUBDIR}/logs/checkpoint.txt
        [ ${T_DIFF} -ge ${DURATION} ] && break

        /usr/bin/node ../updateStreams.js ${CHANNEL_COUNT}
        echo -en "$(date -uIns)\t${SERVER_ID} uS ${ROUND} done\n" >> ${TARGET_SUBDIR}/logs/checkpoint.txt
        /usr/bin/node ../updateEdges.js
        echo -en "$(date -uIns)\t${SERVER_ID} uE ${ROUND} done\n" >> ${TARGET_SUBDIR}/logs/checkpoint.txt
    done

    kill -15 $(cat ${DIR_K}/nordvpn/pid.txt)
    echo -en "$(date -uIns)\t${SERVER_ID} vpn killed\n" >> ${TARGET_SUBDIR}/logs/checkpoint.txt

    sleep 1m
done

exit 0
