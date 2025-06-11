#!/bin/bash


for rfile in `ls root_data/*.root` ; do
    echo $rfile
    python tree_loop.py $rfile
done
