#!/bin/bash

if [ "$1" == "" ]; then
    echo "usage: bash afterCollect.sh dir"
    exit 1
fi
dir="$1"

cd ${dir}
mkdir raws vcnts csvs
mv *-*raw.json raws/.
mv *-*000.csv vcnts/.
mv 17T*.csv csvs/.
mv 18T*.csv csvs/.

cd ..
nohup xz -9 ${dir}/nohup.out >/dev/null 2>&1 &
nohup xz -9 ${dir}/error.err >/dev/null 2>&1 &

sleep 1
echo "All done."
