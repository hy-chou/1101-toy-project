#!/bin/bash

OPT_LAST="3"

for argv in "$@"
do
	[ $argv == "r" ] && [ -f report.txt ] && rm report.txt
	[ $argv == "0" ] && OPT_LAST="0"
done

if [ -f report.txt ] ; then
    cat report.txt
    exit 0
fi

echo "report.sh running..."

LINES="# $(pwd | rev | cut -d / -f 1 | rev)"

LINES=$(echo -e "${LINES}\n\nupdated $(date -Iseconds)")

LINES=$(echo -e "${LINES}\n\n$(python3 ../../analyze/report/report.py ${OPT_LAST})")

LINES=$(echo -e "${LINES}\n\n## du -hd")
LINES=$(echo -e "${LINES}\n\n$(du -hd 0)")

echo "${LINES}" >> report.txt
echo "${LINES}"
