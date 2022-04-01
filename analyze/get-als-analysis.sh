#!/bin/bash

if [ "$1" == "" ]; then
    echo "bad usage"
    exit 1
fi
als="$1"

cat ${als} | grep \ 0:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 1:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 2:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 3:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 4:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 5:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 6:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 7:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 8:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 9:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 10:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 11:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 12:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 13:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 14:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 15:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 16:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 17:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 18:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 19:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 20:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 21:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 22:..:.. | wc -l >> als-ana.txt
cat ${als} | grep \ 23:..:.. | wc -l >> als-ana.txt
