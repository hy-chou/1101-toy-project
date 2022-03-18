#!/bin/bash

t0=$(date --iso-8601="seconds")
top -u samuel | head -n 20 > /home/samuel/${t0}.top
iftop -ts 60 > /home/samuel/${t0}.iftop &

sleep 1
echo "All done."
