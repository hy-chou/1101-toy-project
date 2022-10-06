#!/bin/bash

DIR_C="/etc/openvpn/confs"

TARGET_DIR="$1"
NUM_CHANNEL="$2"

mkdir -p ${TARGET_DIR}/logs
cd ${TARGET_DIR}

for SERVER_ID in "de923" "tw165" "us8926"
do
    /usr/sbin/openvpn \
        --daemon \
        --config     ${DIR_C}/${SERVER_ID}.conf \
        --writepid   ${TARGET_DIR}/logs/openvpn.pid \
        --log-append ${TARGET_DIR}/logs/openvpn.log

    sleep 10

    /usr/bin/node ../updateStreams.js ${NUM_CHANNEL}
    /usr/bin/node ../updateEdges.js

    PID="$(cat ${TARGET_DIR}/logs/openvpn.pid)"

    kill -15 ${PID}
done
