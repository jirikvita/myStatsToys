#!/usr/bin/python

import ROOT

gInfty = 999e999
gEpsilon = 1e-4

gkm = 1.e3
gm = 1.

gMeV = 1.e-3
gGeV = 1. # eV
gTeV = 1.e3 # eV
geV = 1e-9

# https://pdg.lbl.gov/2023/AtomicNuclearProperties/HTML/air_dry_1_atm.html

gX0 = 36.62 # air; g/cm2
gIntLengthGamma = gX0*9./7.

# inelastic
gPiIntLength = 122. # g/cm2
# elastic:
gPiCollisionLength = 88.5 # g/cm2

# inelastic
gHadIntLength = 90.1 # g/cm2
# elastic
gHadCollisionLength = 61.3 # g/cm2

gLength = { 'e' : gX0, 'gamma' : gIntLengthGamma, 'pi' : gPiIntLength, 'mu' : gInfty, 'nu' : gInfty, 'p' : gHadIntLength}
gctau = { 'e' : gInfty, 'gamma' : gInfty, 'pi' : 7.8*gm, 'mu' : 660*gm, 'p' : gInfty }
gmass = { 'e' : 0.511*gMeV, 'gamma' : 0, 'pi' : 139.6*gMeV, 'mu' : 105.7*gMeV, 'nu' : 0., 'p' : 938.3*gMeV}

# critical energy for the EM shower, for electrons
gECEM = 87.92*gMeV
gECpair = 2*gmass['e']


# critical energy to produce pions:
ECpiThr = 20*gGeV

gcol = { 'e' : ROOT.kGreen+2, 'gamma' : ROOT.kAzure-3, 'pi' : ROOT.kRed + 2, 'mu' : ROOT.kMagenta+3, 'nu' : ROOT.kGray+2, 'p' : ROOT.kRed}
glst = { 'e' : 1, 'gamma' : 2, 'pi' : 1, 'mu' : 2, 'nu' : 3, 'p' : 1}
glwd = { 'e' : 1, 'gamma' : 1, 'pi' : 1, 'mu' : 1, 'nu' : 1, 'p' : 1}
glabel = {'e' : 'e^{#pm}', 'gamma' : '#gamma', 'pi' : '#pi^{#pm}', 'mu' : '#mu^{#pm}', 'nu' : '#nu/#bar{#nu}', 'p' : 'p/#bar{p}'}
gdaughters = { 'e' : ['',''], 'gamma' : ['',''], 'pi' : ['mu','nu'], 'mu' : ['e','nu'], 'nu' : ['',''], 'p' : ['','']}

##########################################

class tunables:
    def __init__(self):
        self.PionsConst = 10.
        self.PionsExp = 0.2
        # fraction of energy in collision going to pions:
        self.Inelasticity = 0.35
    def print(self):
        print(self.PionsConst, self.PionsExp, self.Inelasticity)
    def makeTag(self):
        tag = f'_Inel_{self.Inelasticity}_C_{self.PionsConst}_piExp_{self.PionsExp}'
        return tag
        
        
##########################################
