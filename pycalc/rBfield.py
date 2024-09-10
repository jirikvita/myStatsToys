#!/usr/bin/python

from math import sqrt, pow

e = 1.602e-19 # C
eV = 1.*e # J
MeV = 1e6*eV
GeV = 1e9*eV
TeV = 1e12*eV
c = 299792458 # m/s
c2 = pow(c,2)
km = 1e3 # m
m = 1

def getR(M, q, T, B):
    pc = sqrt(T*(T+2*M*c2))
    r = pc / (c*q*B)
    print('Particle of mass {:4.1f}MeV of kinetic energy {:5.1f}MeV has momentum {:5.1} MeV. \nIn B={:}T the track curvature is {:1.3f}km = {:1.3f}m'.format(M*c*c / MeV, T / MeV, pc/MeV, B, r / km, r / m))
    return r

# alpha particle in Earth's magnetic field
q = 2.*e
M = 3.7*GeV / (c2)
T = 5*MeV
B = 50e-6 # T
r = getR(M, q, T, B)

# LHC proton
q = 1.*e
M = 938*MeV / (c2)
T = 6.8*TeV
B = 8 # T
r = getR(M, q, T, B)

