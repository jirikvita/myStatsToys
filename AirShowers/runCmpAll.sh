#!/bin/bash

for gen in EPOS SIBYLL ; do
  for i in `ls | grep root_Inel | grep -v old` ; do
      if [ -d $i ] ; then
  	./cmpXmean.py $i $gen -b
      fi
  done
done
