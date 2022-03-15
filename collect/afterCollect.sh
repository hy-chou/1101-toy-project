#!/bin/bash

if [ "$1" == "" ]; then
    echo "usage: bash afterCollect.sh target_directory"
    exit 1
fi
dir="$1"

cd ${dir}
mkdir csvs raws vcnts dts
mv 2022-*raw.json raws/.
mv 2022-*vcnt*.csv vcnts/.
mv 2022-*dt.csv dts/.
mv *.csv csvs/.

cd ..
nohup xz -9 ${dir}/nohup.out &

sleep 1
echo "All done."
