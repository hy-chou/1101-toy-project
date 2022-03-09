#!/bin/bash

dir="try45"

cd ${dir}
mkdir csvs raws tops dts
mv *raw.* raws/.
mv *top.* *mid.* tops/.
mv *dt.* dts/.
mv *.csv csvs/.

cd ..
nohup xz -9 ${dir}/nohup.out &

sleep 1
echo "All done."
