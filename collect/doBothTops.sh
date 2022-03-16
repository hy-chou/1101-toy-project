#!/bin/bash

t0=$(date --iso-8601="seconds")
top -u samuel | head -n 20 > ${t0}.top
iftop -ts 60 > ${t0}.iftop &

sleep 1
echo "All done."

