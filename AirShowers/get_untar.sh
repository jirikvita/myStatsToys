#!/bin/bash


echo "Getting..."
#~/bin/myget.py zubr "/home/qitek/work/myStatsToys-main/A*/*.tgz"
~/bin/myget.py zubr air.tgz

echo "Untarring..."
#for i in `ls *.tgz` ; do
#    tar xzf $i
#done
tar xzf air.tgz

echo "Moving..."
#mv myStatsToys-main/AirShowers*/r* .
mv AirShowers*/r* .

echo "Cleaning..."

#rmdir myStatsToys-main/AirShowers* myStatsToys-main

rm *.tgz
rm -rf AirShowers*

