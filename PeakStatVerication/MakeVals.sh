#!/bin/bash

if [ $# -lt 1 ] ; then
    echo "Usage:"
    echo "$0 file.C"
    exit 1
fi

i=$1
j=`basename $i .C`.txt
k=`basename $i .C`_vals.txt
echo "Parsing ${i} ..."

echo "Making ${j} ..."
cat $i | grep SetBin | sed "s|histo__1->SetBinContent(||g" | sed "s|);||" | sed "s|,| |" > $j
echo "Making ${k} ..."
cat $j | awk '{print $2};' > $k
