#!/bin/bash

for `ls pdf/*.pdf | grep -v 30` ; do
    rm pdf/$i
done
for `ls png/*.png | grep -v 30` ; do
    rm png/$i
done

rm *.aux *.log *\~
rm root/*.root



