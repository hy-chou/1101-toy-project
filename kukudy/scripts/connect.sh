#!/bin/bash

SERVER_ID="$1"

DIR_N="/etc/openvpn/nordvpn"
CONF="${SERVER_ID}.nordvpn.com.udp.ovpn"
TS="$(date -I)"

/usr/sbin/openvpn                              \
    --config         ${DIR_N}/ovpn_udp/${CONF} \
    --auth-user-pass ${DIR_N}/auth.txt         \
    --log-append     ${DIR_N}/logs/${TS}.log   \
    --writepid       ${DIR_N}/logs/${TS}.pid   \
    --daemon
