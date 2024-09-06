#!/usr/bin/python

import ROOT

gkm = 1.e3
gm = 1.

gMeV = 1.e-3
gGeV = 1. # eV
gTeV = 1.e3 # eV
geV = 1e-9

gX0 = 37. # air; g/cm2
gIntLengthGamma = gX0*9./7.
gIntLengthHad = 120. # g/cm

gLength = { 'e' : gX0, 'gamma' : gIntLengthGamma, 'pi' : gIntLengthHad }

gme = 0.511*gMeV

# critical energy for the EM shower, for electrons
gECEM = 85*gMeV
gECpair = 2*gme

# critical energy to produce pions:
ECpiThr = 20*gGeV

gcol = { 'e' : ROOT.kGreen+2, 'gamma' : ROOT.kBlue, 'pi' : ROOT.kRed, 'mu' : ROOT.kBlue}
glst = { 'e' : 1, 'gamma' : 2, 'pi' : 1, 'mu' : 3}
glwd = { 'e' : 1, 'gamma' : 1, 'pi' : 2, 'mu' : 1}
glabel = {'e' : 'e', 'gamma' : '#gamma', 'pi' : '#pi', 'mu' : '#mu'}
