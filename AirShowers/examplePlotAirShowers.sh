#!/bin/bash
# jk 6.9.2024

batch=0
draw=1
for i in 30 300 3000 30000 300000 ; do
    ./airsim.py $i
done


