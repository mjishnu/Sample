#!/bin/bash

curl -sL https://www.amfiindia.com/spages/NAVAll.txt -o NAVAll.txt

awk -F ';' 'NR > 1 && NF >= 5 { print $4 "\t" $5 }' NAVAll.txt > NAVAll.tsv

echo "Extracted data saved to scheme_nav.tsv"