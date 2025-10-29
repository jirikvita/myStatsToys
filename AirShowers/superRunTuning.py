#!/usr/bin/python3

import os, sys


# jk 29.10.2025



#inels = [0.4, 0.45, 0.5, 0.55, 0.6]
inels = [0.4, 0.45, 0.5, 0.55,0.6]
sigma_inels = [0.2]
Nchs = [ 8, 10, 12]
sigma_Nchs = [2] #, 4]
maxNlengthsEMs = [1.25]
maxNlengthsHads = [1.25, 1.5 ] #, 2]

n=0
for inel in inels:
    for sigma_inel in sigma_inels:
        for Nch in Nchs:
            for sigma_Nch in sigma_Nchs:
                for mlEM in maxNlengthsEMs:
                    for mlHad in maxNlengthsHads:
                        n += 1
                        cmd = f'./runAirShowers.sh {inel} {sigma_inel} {Nch} {sigma_Nch} {mlEM} {mlHad} ' + '&'
                        print(cmd)
                        os.system(cmd)
print(f'Total tunable settings: {n}')
