#!/bin/bash

TARGET_DIR="$1"
NUM_CHANNEL="$2"


DIR_N="/etc/openvpn/nordvpn"
TS="$(date -I)"

mkdir -p ${TARGET_DIR}/logs
cd ${TARGET_DIR}

for _ in {1..5}
do
    for SERVER_ID in "de923" "tw165" "uk1978" "us8926"
    do
        CONF="${SERVER_ID}.nordvpn.com.udp.ovpn"

        /usr/sbin/openvpn                                   \
            --config         "${DIR_N}/ovpn_udp/${CONF}"      \
            --auth-user-pass "${DIR_N}/auth.txt"              \
            --writepid       "${DIR_N}/logs/${TS}.pid"        \
            --log-append     "${TARGET_DIR}/logs/${TS}.log"   \
            --daemon

        /usr/bin/node ../utils/reqVPNStatus.js
        /usr/bin/node ../updateStreams.js ${NUM_CHANNEL}
        /usr/bin/node ../updateEdges.js

        kill -15 "$(cat ${DIR_N}/logs/${TS}.pid)"

        sleep 3
    done
done
