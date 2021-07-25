#! /bin/sh


#cd vars
# python GenCode.py > vars.tex 
#cd ../

MyDate=`date +%y%m%d`

#for file in YieldTables_main ; do
#  latex  ${file}.tex
#  latex  ${file}.tex
#  dvips ${file}.dvi -o ${file}.ps
#  dvipdf  ${file}
#  ps2pdf ${file}.ps
#  mv ${file}.pdf ~/
#done



for file in main ; do
  latex  ${file}.tex
  latex  ${file}.tex
  dvips ${file}.dvi -o ${file}.ps
  dvipdf  ${file}
  ps2pdf ${file}.ps
  mv ${file}.pdf ~/Talk_JiriKvita_${MyDate}.pdf
done

