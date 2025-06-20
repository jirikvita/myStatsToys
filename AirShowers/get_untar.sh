#!/bin/bash


echo "Getting..."
~/bin/myget.py zubr "/home/qitek/work/myStatsToys-main/A*/*.tgz"

echo "Untarring..."
for i in `ls *.tgz` ; do
    tar xzf $i
done

echo "Moving..."
mv myStatsToys-main/AirShowers*/r* .

echo "Cleaning..."

rmdir myStatsToys-main/AirShowers* myStatsToys-main

rm *.tgz


