#!/bin/bash

for CHANNEL in hychou
do
    echo $CHANNEL
    cat ./k5997_100_25Hz/edgs/* | grep "$CHANNEL" >  k5_$CHANNEL.tsv.tmp
    cat ./k5998_100_25Hz/edgs/* | grep "$CHANNEL" >> k5_$CHANNEL.tsv.tmp
    cat ./k5999_100_25Hz/edgs/* | grep "$CHANNEL" >> k5_$CHANNEL.tsv.tmp
    cat ./k6997_100_25Hz/edgs/* | grep "$CHANNEL" >  k6_$CHANNEL.tsv.tmp
    cat ./k6998_100_25Hz/edgs/* | grep "$CHANNEL" >> k6_$CHANNEL.tsv.tmp
    cat ./k6999_100_25Hz/edgs/* | grep "$CHANNEL" >> k6_$CHANNEL.tsv.tmp

    sort -k2 k5_$CHANNEL.tsv.tmp | sort -sk2.19 > k5_$CHANNEL.tsv
    sort -k2 k6_$CHANNEL.tsv.tmp | sort -sk2.19 > k6_$CHANNEL.tsv
    rm *.tmp

    python3 compare.py $CHANNEL
done
