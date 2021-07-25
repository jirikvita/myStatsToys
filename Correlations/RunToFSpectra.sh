#!/bin/bash


for shift in 20mm 15mm 10mm 5mm 1mm ; do
    txt=/home/qitek/cernbox/TimePix/Spectra/Train1_${shift}_15h/ene.txt
    ./DrawSpectra.py $txt ToF_${shift} ToF_${shift} 
done
