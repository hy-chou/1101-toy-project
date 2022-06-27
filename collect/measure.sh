#!/bin/bash

if [ "$1" == "" ] ; then
    echo "usage:  "
    echo "3. sudo su"
    echo "4. nohup bash ../measure.sh SLEEP_TIME > /dev/null 2>&1 &"
    echo ""
    echo -e "SLEEP_TIME\twait SLEEP_TIME until collector starts"
    exit 0
fi

sleep "$1"

for i in {0..13}
do
    date --iso-8601="seconds" >> date.txt
    top -bn 1 | head -n 5 >> top.txt
    iftop -ts 60 | tail -n 4 | head -n 2 >> iftop.txt
    sleep 4m
done
