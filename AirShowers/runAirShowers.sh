#!/bin/bash
# jk 6.9.2024

batch=1
draw=0
for i in 100 1000 10000 ; do #100000 1000000 ; do
#for i in 1000000 ; do #100000 1000000 ; do
    for j in `seq 0 9` ; do
	./airsim.py $i $j $batch $draw
    done
done


