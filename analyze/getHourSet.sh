#!/bin/bash

if [ "$1" == "" ]; then
    echo "bad usage"
    exit 1
fi
dir="$1"

cd ${dir}

for hh in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23
do
  echo ${hh}
  python3 ~/1101-toy-project/analyze/getIPSet.py 12T${hh} > ../2022-03-12T${hh}.iplist
done

sleep 1
echo "All done."
