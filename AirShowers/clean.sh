#!/bin/bash

for `ls pdf/*.pdf *.pdf | grep -v main | grep -v 30` ; do
    rm pdf/$i
done
for `ls png/*.png *.png | grep -v 30` ; do
    rm png/$i
done

rm *.aux *.log *\~
rm root/*.root



