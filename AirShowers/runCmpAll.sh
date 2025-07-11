#!/bin/bash

for gen in EPOS SIBYLL ; do
  for i in `ls | grep root_Inel | grep -v old` ; do
#  for i in `ls nPiLogEi/ | grep root_Inel | grep -v old` ; do
      #if [ -d nPiLogEi/$i ] ; then
	#  echo "*** nPiLogEi/$i ***"
  	#  ./cmpXmean.py nPiLogEi/$i $gen -b
      #fi
      if [ -d $i ] ; then
	  echo "*** nPiLogEi/$i ***"
  	  ./cmpXmean.py $i $gen -b
      fi
  done
done
