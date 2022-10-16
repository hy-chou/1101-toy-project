#!/bin/bash

if [ $# != 1 ] ; then
    echo -e "
SYNOPSIS
    sudo bash connect.sh COUNTRY_CODE
"
    exit 0
fi

DIR_K="/home/nslab-m06/Samuel/1101-toy-project/kukudy"
SERVER_ID="$(/usr/bin/node ${DIR_K}/utils/getServersRecommendations.js $1)"

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
