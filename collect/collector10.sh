#!/bin/bash

if [ "$4" == "" ] ; then
    echo "usage: bash collector10.sh dir dd hh he"
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
cmd="nohup node ../scheduler10.js"

test ! -d ${dir} && mkdir ${dir}
cd ${dir}

while [ ! ${hh} == $((${he}+1)) ]
do
    ${cmd} "00-19/10 ${hh} ${dd} * *" "30 ${hh} ${dd} * *" >/dev/null 2>&1 &
    ${cmd} "20-39/10 ${hh} ${dd} * *" "50 ${hh} ${dd} * *" >/dev/null 2>&1 &
    if [ ${hh} != 23 ] ; then
        ${cmd} "40-59/10 ${hh} ${dd} * *" "10 $((${hh}+1)) ${dd} * *" >/dev/null 2>&1 &
        hh="$((${hh}+1))"
    else
        ${cmd} "40-59/10 23 ${dd} * *" "10 0 $((${dd}+1)) * *" >/dev/null 2>&1 &
        exit 0
    fi
done
