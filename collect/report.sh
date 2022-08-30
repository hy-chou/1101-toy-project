#!/bin/bash

if [ -f report.txt ] ; then
    cat report.txt
		exit 0
fi

echo "report.sh running..."

LINES="# REPORT
$(date -Iseconds)

## File Space Usage

$(du -hd 0)

## Network & Machine

$(python3 ../../analyze/report/report.py)

## Counts
$(echo -e "             \tULG\tULGS\tTSVS\tERRS\tIFTOPS\tTOPS")"

for h in $(ls ulgs)
do
	ULG=$(ls ulgs/$h | wc -l)
	ULGS=$(cat ulgs/$h/* | wc -w)
	TSVS=$(find tsvs/$h -name "*.tsv" | xargs cat | wc -l)
	ERRS=$(find tsvs/$h -name "*.tsv" | xargs cat | cut -f 2 | grep -v "[0-9][.][0-9]\+[.][0-9]\+[.][0-9]" | wc -l)

	IFTOPS=$(cat txts/iftops/${h}iftop.txt | grep 2022 | wc -l)
	TOPS=$(cat txts/tops/${h}top.txt | grep 2022 | wc -l)

	LINES="${LINES}
$(echo -e "$h\t${ULG}\t${ULGS}\t${TSVS}\t${ERRS}\t${IFTOPS}\t${TOPS}")"
done

echo "${LINES}" >> report.txt
echo "${LINES}"
