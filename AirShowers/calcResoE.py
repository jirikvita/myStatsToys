#!/usr/bin/python


from math import log10


mp = 0.938
Ms = [100, 100, 100, 1000, 1000, 1000, 1000] # GeV
Gammas = [10, 3, 2, 1, 100, 30, 20, 10]

for M, gamma in zip(Ms, Gammas):
    Eres = pow(M, 2) / (2*mp)
    Eres0 = pow(M - gamma, 2) / (2*mp)
    Eres1 = pow(M + gamma, 2) / (2*mp)
    print(f'Mass: {M}, resonant energies E0,E,E1: {Eres0:.0f}, {Eres:.0f}, {Eres1:.0f} GeV')
    print(f'   i.e. for M={M} and Gamma={gamma} in logE:            : [{log10(Eres0)+9:.3f}, {log10(Eres1)+9:.3f}], center at {log10(Eres1)+9:.2f}')

    
    
