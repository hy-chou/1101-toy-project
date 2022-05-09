#!/bin/bash

if [ "$1" == "" ]; then
    echo "usage: bash doCollect10s10k.sh dir"
    exit 1
fi
dir="$1"

dd="99"
hh="0"
he="23"

cmd1="nohup node ../scheduler.js 0001 1000"
cmd2="nohup node ../scheduler.js 1001 2000"
cmd3="nohup node ../scheduler.js 2001 3000"
cmd4="nohup node ../scheduler.js 3001 4000"
cmd5="nohup node ../scheduler.js 4001 5000"
cmd6="nohup node ../scheduler.js 5001 6000"
cmd7="nohup node ../scheduler.js 6001 7000"
cmd8="nohup node ../scheduler.js 7001 8000"
cmd9="nohup node ../scheduler.js 8001 9000"
cmd10="nohup node ../scheduler.js 9001 10000"

test ! -d ${dir} && mkdir ${dir}
cd ${dir}

while [ ${hh} != $((${he}+1)) ]
do
    ${cmd1} "*/10 00-19 ${hh} ${dd} * *" "0 30 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd2} "*/10 00-19 ${hh} ${dd} * *" "0 30 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd3} "*/10 00-19 ${hh} ${dd} * *" "0 30 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd4} "*/10 00-19 ${hh} ${dd} * *" "0 30 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd5} "*/10 00-19 ${hh} ${dd} * *" "0 30 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd6} "*/10 00-19 ${hh} ${dd} * *" "0 30 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd7} "*/10 00-19 ${hh} ${dd} * *" "0 30 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd8} "*/10 00-19 ${hh} ${dd} * *" "0 30 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd9} "*/10 00-19 ${hh} ${dd} * *" "0 30 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd10} "*/10 00-19 ${hh} ${dd} * *" "0 30 ${hh} ${dd} * *" >/dev/null 2>&1 &

    ${cmd1} "*/10 20-39 ${hh} ${dd} * *" "0 50 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd2} "*/10 20-39 ${hh} ${dd} * *" "0 50 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd3} "*/10 20-39 ${hh} ${dd} * *" "0 50 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd4} "*/10 20-39 ${hh} ${dd} * *" "0 50 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd5} "*/10 20-39 ${hh} ${dd} * *" "0 50 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd6} "*/10 20-39 ${hh} ${dd} * *" "0 50 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd7} "*/10 20-39 ${hh} ${dd} * *" "0 50 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd8} "*/10 20-39 ${hh} ${dd} * *" "0 50 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd9} "*/10 20-39 ${hh} ${dd} * *" "0 50 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd10} "*/10 20-39 ${hh} ${dd} * *" "0 50 ${hh} ${dd} * *" >/dev/null 2>&1 &

    if [ ${hh} != 23 ]; then
        ${cmd1} "*/10 40-59 ${hh} ${dd} * *" "0 10 $((${hh}+1)) ${dd} * *" >/dev/null 2>&1 &
        ${cmd2} "*/10 40-59 ${hh} ${dd} * *" "0 10 $((${hh}+1)) ${dd} * *" >/dev/null 2>&1 &
        ${cmd3} "*/10 40-59 ${hh} ${dd} * *" "0 10 $((${hh}+1)) ${dd} * *" >/dev/null 2>&1 &
        ${cmd4} "*/10 40-59 ${hh} ${dd} * *" "0 10 $((${hh}+1)) ${dd} * *" >/dev/null 2>&1 &
        ${cmd5} "*/10 40-59 ${hh} ${dd} * *" "0 10 $((${hh}+1)) ${dd} * *" >/dev/null 2>&1 &
        ${cmd6} "*/10 40-59 ${hh} ${dd} * *" "0 10 $((${hh}+1)) ${dd} * *" >/dev/null 2>&1 &
        ${cmd7} "*/10 40-59 ${hh} ${dd} * *" "0 10 $((${hh}+1)) ${dd} * *" >/dev/null 2>&1 &
        ${cmd8} "*/10 40-59 ${hh} ${dd} * *" "0 10 $((${hh}+1)) ${dd} * *" >/dev/null 2>&1 &
        ${cmd9} "*/10 40-59 ${hh} ${dd} * *" "0 10 $((${hh}+1)) ${dd} * *" >/dev/null 2>&1 &
        ${cmd10} "*/10 40-59 ${hh} ${dd} * *" "0 10 $((${hh}+1)) ${dd} * *" >/dev/null 2>&1 &

        hh="$((${hh}+1))"
    else
        ${cmd1} "*/10 40-59 23 ${dd} * *" "0 10 0 $((${dd}+1)) * *" >/dev/null 2>&1 &
        ${cmd2} "*/10 40-59 23 ${dd} * *" "0 10 0 $((${dd}+1)) * *" >/dev/null 2>&1 &
        ${cmd3} "*/10 40-59 23 ${dd} * *" "0 10 0 $((${dd}+1)) * *" >/dev/null 2>&1 &
        ${cmd4} "*/10 40-59 23 ${dd} * *" "0 10 0 $((${dd}+1)) * *" >/dev/null 2>&1 &
        ${cmd5} "*/10 40-59 23 ${dd} * *" "0 10 0 $((${dd}+1)) * *" >/dev/null 2>&1 &
        ${cmd6} "*/10 40-59 23 ${dd} * *" "0 10 0 $((${dd}+1)) * *" >/dev/null 2>&1 &
        ${cmd7} "*/10 40-59 23 ${dd} * *" "0 10 0 $((${dd}+1)) * *" >/dev/null 2>&1 &
        ${cmd8} "*/10 40-59 23 ${dd} * *" "0 10 0 $((${dd}+1)) * *" >/dev/null 2>&1 &
        ${cmd9} "*/10 40-59 23 ${dd} * *" "0 10 0 $((${dd}+1)) * *" >/dev/null 2>&1 &
        ${cmd10} "*/10 40-59 23 ${dd} * *" "0 10 0 $((${dd}+1)) * *" >/dev/null 2>&1 &

        sleep 1
        echo "All done."
        exit 0
    fi
done

sleep 1
echo "All done."
