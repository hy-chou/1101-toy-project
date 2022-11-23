#!/bin/bash

if [ $# != 1 ] ; then
    echo -en "
DIRECTIONS
  \tWrite the following lines to /etc/cron.d/kukudy

DIR_K=$(cd .. && pwd)

*    * * * * $USER bash \${DIR_K}/scripts/bookcss-ce.sh \${DIR_K}/l1001_7_1min
"
    exit 0
fi

mkdir -p $1/logs && cd $1

echo -en "$(head -n1 ../.env)\n"     >> $1/logs/checkpoint.txt

node ../updateSpecificStreams.js
echo -en "$(date -uIns)\tuSS done\n" >> $1/logs/checkpoint.txt

node ../updateEdges.js
echo -en "$(date -uIns)\tuE  done\n" >> $1/logs/checkpoint.txt
