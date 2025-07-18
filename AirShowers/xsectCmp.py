#!/usr/bin/python

# jk 25.6.2025


from consts import *

ls = {
    'Electron radiative losses' : gX0,
    'Photon conversion' : gIntLengthGamma,
    'Pion nuclear interaction length' : gPiIntLength,
    'Proton nuclear interaction length' : gHadIntLength,
}


for name,l in ls.items():
    xsect = airA / (l*NA) # cm^2
    xsect_mb = float(xsect*1e27)
    #print(f'{name:25}: xsect={xsect:1.3} cm2 = {xsect_mb:3.1f} mb')
    print(f'{name:35} & {l:1.1f}' + r' $\mathrm{g/cm}^2$ ' + f' &  {l/airRho/100:1.0f} m  &   {xsect_mb:3.0f} mb' + r' \\')
