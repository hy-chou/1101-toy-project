#!/bin/bash

du -hd 0
echo
test ! -d tsvs && mkdir tsvs || echo "tsvs/ exists"
test ! -d txts && mkdir txts || echo "txts/ exists"
test ! -d ulgs && mkdir ulgs || echo "ulgs/ exists"
test -f 2*    && mv 2*    tsvs/ || echo "2* DNE"
test -f *.txt && mv *.txt txts/ || echo "*.txt DNE"
test -f u*v   && mv u*v   ulgs/ || echo "u*v DNE"
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
