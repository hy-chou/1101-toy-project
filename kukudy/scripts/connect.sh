#!/bin/bash

if [ $# != 2 ] ; then
    echo -e "
SYNOPSIS
    sudo bash connect.sh PATH_TO_KUKUDY COUNTRY_CODE
"
    exit 0
fi

DIR_K="$1"
SERVER_ID="$(/usr/bin/node ${DIR_K}/utils/getServersRecommendations.js $2)"

if [ $? == 1 ] ; then
    exit 0
fi

DIR_N="/etc/openvpn/nordvpn"
CONF="${SERVER_ID}.nordvpn.com.udp.ovpn"
TS="$(date -I)"

/usr/sbin/openvpn                              \
    --config         ${DIR_N}/ovpn_udp/${CONF} \
    --auth-user-pass ${DIR_N}/auth.txt         \
    --log-append     ${DIR_N}/logs/${TS}.log   \
    --writepid       ${DIR_N}/logs/${TS}.pid   \
    --daemon
