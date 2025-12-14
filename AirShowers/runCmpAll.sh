#!/bin/bash

for gen in EPOS ; do
#for gen in EPOS SIBYLL ; do
    # no Zprime:
    #for i in `ls | grep root_Inel | grep -v old | grep -v Zprime` ; do
    # Zprime
    #for i in `ls | grep root_Inel | grep -v old | grep Zprime` ; do
    # Em signal truncation test:
    #for i in `ls | grep root_Inel | grep -v old | grep EM` ; do
    #for i in `ls | grep root_Inel | grep EM1.125 | grep -v prim` ; do
    #for i in `ls | grep root_Inel | egrep "C_2|C_4|C_6" | grep -v prim` ; do

#        for i in `ls | grep root_Inel | grep Zprime_100.0` ; do
#        for i in `ls | grep root_Inel | grep Zprime_1000.0` ; do


#DEFAULT!
    for i in `ls | grep root_Inel | grep 999 | egrep  "Zprime|NoNewPhys" ` ; do

#	for i in `ls | grep root_Inel | grep 999 | egrep  "Zprime" ` ; do

	    
	#    for i in `ls | grep root_Inel | grep  Zprime | grep Gamma_1.0` ; do
# for i in `ls | grep root_Inel | grep  Zprime | grep Gamma_3` ; do

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
