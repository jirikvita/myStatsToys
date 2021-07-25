#!/bin/bash

# jesyne 2016 separate spectra and particle species correlations:
./AlfaBetaGama.py Bg_abg.txt Bg
./AlfaBetaGama.py abg_jeskyne.txt Jeskyne

# jeskyne 2017, all spectra available only:
./DrawSpectra_single.py ene_jeskyneII.txt


# muons on the ground:
# extended:
./DrawSpectra.py  "MuSearch_570x600s_14_ene.txt MuSearch_324x600_16_ene.txt" MuSearchAll "10min windows" extended

# flights:
# extended:
# number of 30s exposures: NY there and back, DG-MEX there and back, and Prg-Wien-Zur-GVA Oct 2017
# In [2]: 333+80+60+400+300+120+142+100+40+270 + 50+88+30+116
# Out[2]: 2129
# i.e. 1064.5 minutes =  17.74166h = 17h 44min 30s
# data sources:
# /home/qitek/cernbox/TimePix/Spectra/CDGMEX (three sets!)
# /home/qitek/cernbox/TimePix/Spectra/MexCdg300x30s_etx/ (three sets!)
# /home/qitek/cernbox/TimePix/Spectra/LetNY_333x30s
# /home/qitek/cernbox/TimePix/Spectra/LetNY_400x30s
# /home/qitek/cernbox/TimePix/Spectra/LetNY_60x30s
# /home/qitek/cernbox/TimePix/Spectra/LetNY_80x30s
# /home/qitek/cernbox/TimePix/Spectra/LetPepaPetrOct2017/PRGWien_50x30_ene.txt
# /home/qitek/cernbox/TimePix/Spectra/LetPepaPetrOct2017/WienGVA_30x30_ene.txt
# /home/qitek/cernbox/TimePix/Spectra/LetPepaPetrOct2017/WienGVA_88x30_ene.txt
# /home/qitek/cernbox/TimePix/Spectra/LetPepaPetrOct2017/ZurPRG_116x30_ene.txt


#./DrawSpectra.py  "LetNY_333x30s_ene.txt  LetNY_400x30s_ene.txt  LetNY_60x30s_ene.txt  LetNY_80x30s_ene.txt MexCdg300x30s_etx_ene1.txt  MexCdg300x30s_etx_ene2.txt  MexCdg300x30s_etx_ene3.txt CDGMEX_ene1.txt CDGMEX_ene3.txt CDGMEX_ene2.txt" AllLongHaulFlights "30s windows" extended


./DrawSpectra.py  "LetNY_333x30s_ene.txt  LetNY_400x30s_ene.txt  LetNY_60x30s_ene.txt  LetNY_80x30s_ene.txt MexCdg300x30s_etx_ene1.txt  MexCdg300x30s_etx_ene2.txt  MexCdg300x30s_etx_ene3.txt CDGMEX_ene1.txt CDGMEX_ene3.txt CDGMEX_ene2.txt PRGWien_50x30_ene.txt WienGVA_30x30_ene.txt WienGVA_88x30_ene.txt ZurPRG_116x30_ene.txt" AllExtFlights "30s windows" extended


# Americium:
# standard:
./DrawSpectra.py "AmClosest_1.txt AmClosest_2.txt" SpectraAmericium "fractions of second" default

# Bg MEX:
./DrawSpectra.py BgMex_270x300x_open_standard_ene.txt SpectraBgMEX "5min windows" default


# Uglass1
./DrawSpectra.py Uglass8h_spect.txt SpectraUglass1 "10min windows" default

