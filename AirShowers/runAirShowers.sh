#!/bin/bash
# jk 6.9.2024

batch=1
for i in 100 1000 10000 100000 1000000 ; do
#for i in 200000 ; do
    for j in `seq 0 49` ; do
	draw=0
	#if [ $j -gt 0 ] ; then
	#    draw=0
	#fi
	#if [ $i -gt 100000 ] ; then
	#    draw=0
	#fi
	./airsim.py $i $j $batch $draw
    done
done

