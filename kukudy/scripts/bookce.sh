#!/bin/bash

if [ $# != 1 ] ; then
    echo -en "
DIRECTIONS
  \tWrite the following lines to /etc/cron.d/kukudy

DIR_K=$(cd .. && pwd)

*    * * * * $USER bash \${DIR_K}/scripts/bookce.sh \${DIR_K}/k0000_100
"
    exit 0
fi

mkdir -p $1 && cd $1
node ../updateEdges.js &
