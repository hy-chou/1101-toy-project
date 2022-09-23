#!/bin/bash

if [ $# != 3 ] ; then
    echo -en "
DIRECTIONS
  \tWrite the following lines to /etc/cron.d/bookc

DIR_C=$(cd .. && pwd)

* * * * * $USER bash \${DIR_C}/books/bookce.sh \${DIR_C}/try0000_1k 1 1000
"
    exit 0
fi

mkdir -p $1 && cd $1
nohup node ../getActiveEdges.js $2 $3 &
