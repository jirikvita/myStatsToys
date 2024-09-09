#!/usr/bin/python

import ROOT

gInfty = 999e999

gkm = 1.e3
gm = 1.

gMeV = 1.e-3
gGeV = 1. # eV
gTeV = 1.e3 # eV
geV = 1e-9

gX0 = 37. # air; g/cm2
gIntLengthGamma = gX0*9./7.
gIntLengthHad = 120. # g/cm

gLength = { 'e' : gX0, 'gamma' : gIntLengthGamma, 'pi' : gIntLengthHad, 'mu' : gInfty, 'nu' : gInfty, 'p' : gIntLengthHad}
gctau = { 'e' : gInfty, 'gamma' : gInfty, 'pi' : 7.8*gm, 'mu' : 660*gm, 'p' : gInfty }
gmass = { 'e' : 0.511*gMeV, 'gamma' : 0, 'pi' : 139.6*gMeV, 'mu' : 105.7*gMeV, 'nu' : 0., 'p' : 938.3*gMeV}

# critical energy for the EM shower, for electrons
gECEM = 85*gMeV
gECpair = 2*gmass['e']

# fraction of energy in collision going to pions:
gInelasticity = 0.45

# critical energy to produce pions:
ECpiThr = 20*gGeV

gcol = { 'e' : ROOT.kGreen+2, 'gamma' : ROOT.kAzure-3, 'pi' : ROOT.kRed + 2, 'mu' : ROOT.kMagenta+3, 'nu' : ROOT.kGray+2, 'p' : ROOT.kRed}
glst = { 'e' : 1, 'gamma' : 2, 'pi' : 1, 'mu' : 2, 'nu' : 3, 'p' : 1}
glwd = { 'e' : 1, 'gamma' : 1, 'pi' : 1, 'mu' : 1, 'nu' : 1, 'p' : 2}
glabel = {'e' : 'e', 'gamma' : '#gamma', 'pi' : '#pi', 'mu' : '#mu', 'nu' : '#nu', 'p' : 'p'}
