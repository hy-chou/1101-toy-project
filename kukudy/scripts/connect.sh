#!/bin/bash

DIR_C="/etc/openvpn/confs"

SERVER_ID="$1"
TARGET_DIR="$2"
NUM_CHANNEL="$3"


mkdir -p ${TARGET_DIR}/logs
cd ${TARGET_DIR}

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
