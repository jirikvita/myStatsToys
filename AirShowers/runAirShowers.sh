#!/bin/bash
# jk 6.9.2024, 16.7.2025

batch=1
for i in 11 11.5 12 12.5 13 13.5 14 14.5 15 15.5 16  ; do
#    for i in 16 15.5 ; do
#    for i in 16 ; do
#    for i in 15.5 ; do
    for j in `seq 0 100` ; do
	draw=0
	#if [ $j -gt 0 ] ; then
	#    draw=0
	#fi
	#if [ $i -gt 100000 ] ; then
	#    draw=0
	#fi
	python3 ./run_airsim.py $i $j $batch $draw >& log_airsim_logE${i}_iter${j}.txt
    done
done


