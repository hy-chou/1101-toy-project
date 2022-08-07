#!/bin/bash

du -hd 0
echo
mkdir tsvs
mkdir txts
mkdir ulgs
mv 2*    tsvs/
mv *.txt txts/
mv u*v   ulgs/
echo
python3 ../../analyze/report_all.py
echo
ls ulgs/ | wc -l
echo
cat ulgs/* | wc -w
echo
cat tsvs/* | wc -l
echo
cat tsvs/* | cut -f 2 | sort | uniq -c
echo
sleep 1
echo "all done."
