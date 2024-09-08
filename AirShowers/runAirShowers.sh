#!/bin/bash
# jk 6.9.2024

batch=1
for i in 100 1000 10000 100000 250000 ; do
#for i in 10000 ; do #100000 1000000 ; do
    for j in `seq 0 50` ; do
	draw=1
	if [ $j -gt 0 ] ; then
	    draw=0
	fi
	if [ $i -gt 100000 ] ; then
	    draw=0
	fi
	./airsim.py $i $j $batch $draw
    done
done


