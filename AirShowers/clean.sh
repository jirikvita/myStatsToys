#!/bin/bash

for i in `ls pdf/*.pdf | grep -v 30` ; do
    rm $i
done
for i in `ls png/*.png | grep -v 30` ; do
    rm $i
done

rm *.aux *.log *\~
rm root/*.root



