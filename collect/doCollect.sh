#!/bin/bash

dir="try99"
hh="0"
he="23"
cmd1="nohup node ../scheduleTop.js"
cmd2="nohup node ../scheduleMid.js"

test ! -d ${dir} && mkdir ${dir}
cd ${dir}

while [ ${hh} != $(($((${he}+1))%24)) ]
do
    ${cmd1} "* 00-19 ${hh} * * *" "0 30 ${hh} * * *" &
    ${cmd2} "* 00-19 ${hh} * * *" "0 30 ${hh} * * *" &
    ${cmd1} "* 20-39 ${hh} * * *" "0 50 ${hh} * * *" &
    ${cmd2} "* 20-39 ${hh} * * *" "0 50 ${hh} * * *" &
    ${cmd1} "* 40-59 ${hh} * * *" "0 10 $(($((${hh}+1))%24)) * * *" &
    ${cmd2} "* 40-59 ${hh} * * *" "0 10 $(($((${hh}+1))%24)) * * *" &
    hh="$(($((${hh}+1))%24))"
done

sleep 1
echo "All done."
