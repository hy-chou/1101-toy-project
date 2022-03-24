#!/bin/bash

t0=$(date --iso-8601="seconds")
top -u samuel | head -n 20 > /home/samuel/${t0}.top
nohup iftop -ts 60 > /home/samuel/${t0}.iftop 2>&1 &

sleep 1
echo "All done."
