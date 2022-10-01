#!/bin/bash

if [ $# != 2 ] ; then
    echo -en "
DIRECTIONS
  \tWrite the following lines to /etc/cron.d/bookc

DIR_C=$(cd .. && pwd)

*/12 * * * * $USER bash \${DIR_C}/books/bookcs.sh \${DIR_C}/try0000_1k 1000
"
    exit 0
fi

mkdir -p $1 && cd $1
node ../updateStreams.js $2 &
