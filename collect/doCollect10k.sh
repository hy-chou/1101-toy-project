#!/bin/bash

if [ "$1" == "" ]; then
    echo "usage: bash doCollect10k.sh dir"
    exit 1
fi
dir="$1"

dd="99"
hh="0"
he="23"

cmd="nohup node ../scheduler10k.js"

test ! -d ${dir} && mkdir ${dir}
cd ${dir}

while [ ${hh} != $((${he}+1)) ]
do
    ${cmd} "0 00-19/2 ${hh} ${dd} * *" "0 35 ${hh} ${dd} * *" &
    ${cmd} "0 20-39/2 ${hh} ${dd} * *" "0 55 ${hh} ${dd} * *" &
    if [ ${hh} != 23 ]; then
        ${cmd} "0 40-59/2 ${hh} ${dd} * *" "0 15 $((${hh}+1)) ${dd} * *" &
        hh="$((${hh}+1))"
    else
        ${cmd} "0 40-59/2 23 ${dd} * *" "0 15 0 $((${dd}+1)) * *" &
        sleep 1
        echo "All done."
        exit 0
    fi
done

sleep 1
echo "All done."
