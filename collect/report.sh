#!/bin/bash

if [ -f report.txt ]; then
    cat report.txt
    exit 0
fi

echo "report.sh running..."

LINES="# $(pwd | rev | cut -d / -f 1 | rev)"

LINES=$(echo -e "${LINES}\n\nupdated $(date -Iseconds)")

LINES=$(echo -e "${LINES}\n\n$(python3 ../../analyze/report/report.py)")

LINES=$(echo -e "${LINES}\n\n## du -hd")
LINES=$(echo -e "${LINES}\n\n$(du -hd 0)")

echo "${LINES}" >> report.txt
echo "${LINES}"
