#!/bin/bash

if [ "$4" == "" ]; then
    echo "usage: bash doCollect3s1k.sh dir dd hh he"
    echo ""
    echo -e "dir\ttarget directory"
    echo -e "dd\tlocal date"
    echo -e "[hh, he]\n\tlocal hour"
    exit 0
fi

dir="$1"
dd="$2"
hh="$3"
he="$4"
cmd="nohup node ../scheduler1k.js"

test ! -d ${dir} && mkdir ${dir}
cd ${dir}

while [ ! ${hh} == $((${he}+1)) ]
do
    ${cmd} "*/3 00-19 ${hh} ${dd} * *" "0 35 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd} "*/3 20-39 ${hh} ${dd} * *" "0 55 ${hh} ${dd} * *" >/dev/null 2>&1 &
    if [ ${hh} != 23 ]; then
        ${cmd} "*/3 40-59 ${hh} ${dd} * *" "0 15 $((${hh}+1)) ${dd} * *" >/dev/null 2>&1 &
        hh="$((${hh}+1))"
    else
        ${cmd} "*/3 40-59 23 ${dd} * *" "0 15 0 $((${dd}+1)) * *" >/dev/null 2>&1 &
        sleep 1
        echo "All done."
        exit 0
    fi
done

sleep 1
echo "All done."
