#!/bin/bash

if [ $# != 2 ] ; then
    echo -en "
DIRECTIONS
  \tWrite the following lines to /etc/cron.d/kukudy

DIR_K=$(cd .. && pwd)

*/10 * * * * $USER bash \${DIR_K}/scripts/bookc.sh \${DIR_K}/k0000_100 100
"
    exit 0
fi

mkdir -p $1 && cd $1
node ../updateStreams.js $2
node ../updateEdges.js
