#!/bin/bash

du -hd 0

mkdir tsvs txts ulgs
mv 2* tsvs/
mv *.txt txts/
mv u*v ulgs/

python3 ../../analyze/report_all.py

cat ulgs/* | wc -w

cat tsvs/* | wc -l

cat tsvs/* | cut -f 2 | sort | uniq -c

sleep 1
echo "all done."
