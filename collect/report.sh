#!/bin/bash

echo "report.sh started."
touch report.txt

du -hd 0 >> report.txt
echo -e "\n-=-\n" >> report.txt
python3 ../../analyze/report/report.py  >> report.txt
echo -e "\n-=-\n" >> report.txt
echo -e "             \tULG\tULGS\tTSVS\tERRS" >> report.txt
for h in $(ls ulgs)
do
	ULG=$(ls ulgs/$h | wc -l)
	ULGS=$(cat ulgs/$h/* | wc -w)
	TSVS=$(find tsvs/$h -name "*.tsv" | xargs cat | wc -l)
	ERRS=$(find tsvs/$h -name "*.tsv" | xargs cat | cut -f 2 | grep -v "[0-9][.][0-9]\+[.][0-9]\+[.][0-9]" | wc -l)
	echo -e "$h\t${ULG}\t${ULGS}\t${TSVS}\t${ERRS}" >> report.txt
done

echo "report.sh done."
cat report.txt
