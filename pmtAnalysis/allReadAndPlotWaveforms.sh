#!/bin/bash

for i in `ls lecroy/LED_test/*.txt` ; do

  python readLecroyWaveforms.py $i -b
    
done


