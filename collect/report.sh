#!/bin/bash

du -hd 0
echo -e "\n-=-\n"

python3 ../../analyze/report/report.py
echo -e "\n-=-\n"

echo -e "             \tULG\tULGS\tTSVS\tERRS"
for h in $(ls ulgs)
do
	ULG=$(ls ulgs/$h | wc -l)
	ULGS=$(cat ulgs/$h/* | wc -w)
	TSVS=$(find tsvs/$h -name "*.tsv" | xargs cat | wc -l)
	ERRS=$(find tsvs/$h -name "*.tsv" | xargs cat | cut -f 2 | grep -v "[0-9][.][0-9]\+[.][0-9]\+[.][0-9]" | wc -l)
	echo -e "$h\t${ULG}\t${ULGS}\t${TSVS}\t${ERRS}"
done
