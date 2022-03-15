#!/bin/bash

if [ "$1" == "" ]; then
    echo "usage: bash afterCollect.sh dir hh he dd"
    exit 1
fi
dir="$1"

hh="0"
he="23"
dd="*"

cmd1="nohup node ../scheduler.js 0001 1000"
cmd2="nohup node ../scheduler.js 1001 2000"
cmd3="nohup node ../scheduler.js 2001 3000"
cmd4="nohup node ../scheduler.js 3001 4000"

test ! -d ${dir} && mkdir ${dir}
cd ${dir}

while [ ${hh} != 24 ]
do
    ${cmd1} "* 00-19 ${hh} ${dd} * *" "0 35 ${hh} ${dd} * *" &
    ${cmd2} "* 00-19 ${hh} ${dd} * *" "0 35 ${hh} ${dd} * *" &
    ${cmd3} "* 00-19 ${hh} ${dd} * *" "0 35 ${hh} ${dd} * *" &
    ${cmd4} "* 00-19 ${hh} ${dd} * *" "0 35 ${hh} ${dd} * *" &

    ${cmd1} "* 20-39 ${hh} ${dd} * *" "0 55 ${hh} ${dd} * *" &
    ${cmd2} "* 20-39 ${hh} ${dd} * *" "0 55 ${hh} ${dd} * *" &
    ${cmd3} "* 20-39 ${hh} ${dd} * *" "0 55 ${hh} ${dd} * *" &
    ${cmd4} "* 20-39 ${hh} ${dd} * *" "0 55 ${hh} ${dd} * *" &

    if [ ${hh} == 23 ]; then
        ${cmd1} "* 40-59 23 ${dd} * *" "0 15 0 $((${dd}+1)) * *" &
        ${cmd2} "* 40-59 23 ${dd} * *" "0 15 0 $((${dd}+1)) * *" &
        ${cmd3} "* 40-59 23 ${dd} * *" "0 15 0 $((${dd}+1)) * *" &
        ${cmd4} "* 40-59 23 ${dd} * *" "0 15 0 $((${dd}+1)) * *" &
    else
        ${cmd1} "* 40-59 ${hh} ${dd} * *" "0 15 $((${hh}+1)) ${dd} * *" &
        ${cmd2} "* 40-59 ${hh} ${dd} * *" "0 15 $((${hh}+1)) ${dd} * *" &
        ${cmd3} "* 40-59 ${hh} ${dd} * *" "0 15 $((${hh}+1)) ${dd} * *" &
        ${cmd4} "* 40-59 ${hh} ${dd} * *" "0 15 $((${hh}+1)) ${dd} * *" &
    fi

    hh="$((${hh}+1))"
done


sleep 1
echo "All done."
