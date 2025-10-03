#!/bin/bash

for gen in EPOS SIBYLL ; do
    # no Zprime:
    #for i in `ls | grep root_Inel | grep -v old | grep -v Zprime` ; do
    # Zprime
    for i in `ls | grep root_Inel | grep -v old | grep Zprime` ; do
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
