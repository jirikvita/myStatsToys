#!/bin/bash
# jk 6.9.2024

batch=1
#for i in 100 1000 10000 100000 1000000 ; do
#for i in 200000 ; do
    for i in 50000 ; do
    for j in `seq 1001 2000` ; do
	draw=1
	#if [ $j -gt 0 ] ; then
	#    draw=0
	#fi
	#if [ $i -gt 100000 ] ; then
	#    draw=0
	#fi
	./run_airsim.py $i $j $batch $draw
    done
done


