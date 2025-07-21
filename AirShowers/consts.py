#!/usr/bin/python

import ROOT
from enum import Enum

from math import log10, pow, sqrt

gInfty = 999e999
gEpsilon = 1e-4

NA = 6.02214076e23

# https://www.engineeringtoolbox.com/molecular-mass-air-d_679.html
airA = 28.9647
airRho = 1.233e-3 # g/cm3

gkm = 1.e3
gm = 1.

gMeV = 1.e-3 # GeV
gGeV = 1. # GeV
gTeV = 1.e3 # GeV
geV = 1e-9 # GeV

# https://pdg.lbl.gov/2023/AtomicNuclearProperties/HTML/air_dry_1_atm.html

gX0 = 37. # 36.62 # air; g/cm2 # Mattews: 37
gIntLengthGamma = gX0*9./7.

# inelastic
gPiIntLength = 120. # 122 g/cm2 # Mattews 2005: 120

# elastic:
#gPiCollisionLength = 88.5 # g/cm2

# inelastic
gHadIntLength = 80. # 90.1 # g/cm2 # Leroy-Rancoita: 80

# elastic -- not needed
#gHadCollisionLength = 61.3 # g/cm2

gLength = { 'e' : gX0,
            'gamma' : gIntLengthGamma,
            'pi' : gPiIntLength,
            'Pi' : gPiIntLength,
            'mu' : gInfty,
            'nu' : gInfty,
            'p' : gHadIntLength}
gctau = { 'e' : gInfty,
          'gamma' : gInfty,
          'pi' : 7.8*gm,
          'Pi' : 7.8*gm,
          'mu' : 660*gm,
          'p' : gInfty }
gmass = { 'e' : 0.511*gMeV,
          'gamma' : 0,
          'pi' : 139.6*gMeV,
          'Pi' : 139.6*gMeV,
          'mu' : 105.7*gMeV,
          'nu' : 0.,
          'p' : 938.3*gMeV}

# critical energy for the EM shower, for electrons
gECEM = 87.92*gMeV # Matthews 2005: 85 # Leroy-Rancoita: 81
gECpair = 2*gmass['e']


# critical energy to produce pions:
ECpiThr = 20*gGeV # as Matthews 2005

gcol = { 'e' : ROOT.kGreen+2,
         'gamma' : ROOT.kAzure-3,
         'pi' : ROOT.kRed + 2,
         'Pi' : ROOT.kYellow,
         'mu' : ROOT.kMagenta+3,
         'nu' : ROOT.kGray+2, 'p' : ROOT.kRed}

glst = { 'e' : 1, 'gamma' : 2, 'pi' : 1, 'Pi' : 1, 'mu' : 2, 'nu' : 3, 'p' : 1}
glwd = { 'e' : 1, 'gamma' : 1, 'pi' : 1, 'Pi' : 1, 'mu' : 1, 'nu' : 1, 'p' : 1}
glabel = {'e' : 'e^{#pm}', 'gamma' : '#gamma', 'pi' : '#pi^{#pm}', 'Pi' : 'res. #pi^{#pm}', 'mu' : '#mu^{#pm}', 'nu' : '#nu/#bar{#nu}', 'p' : 'p/#bar{p}'}

gdaughters = { 'e' : ['',''], 'gamma' : ['',''], 'pi' : ['mu','nu'], 'Pi' : ['mu','nu'], 'mu' : ['e','nu'], 'nu' : ['',''], 'p' : ['',''] }



##########################################

class decayModes(Enum):
    kPiPi = 0
    kMuMu = 1
    kee = 2
decays = {decayModes.kPiPi: 'pipi',
          decayModes.kMuMu: 'mumu',
          decayModes.kee: 'ee'}

##########################################

class tunables:
    def __init__(self):

        # hadroproduction parameters
        # fraction of energy in collision going to pions:
        self.Inelasticity = 0.55
        self.sigmaInelasticity = 0.2
        # for the pion number logarithmic dependence on energy
        self.PionsConst = 120.
        self.sigmaPionConst = 30.
        
        # new physics
        self.doNewPhysics = True
        self.MZprimeHadXsectFraction = 0.1
        self.MZprime = 100*gGeV
        self.GammaZprime = 0.1*self.MZprime
        self.decayMode = decayModes.kPiPi
        #self.decayMode = decayModes.kMumu
        #self.decayMode = decayModes.kee
        
        
    def print(self):
        print(self.PionsConst, self.PionsExp, self.Inelasticity)
    def makeTag(self):
        tag = f'_Inel_{self.Inelasticity}_sigmaInel_{self.sigmaInelasticity}_C_{self.PionsConst}_Csigma_{self.sigmaPionConst}' #_piExp_{self.PionsExp}'
        if self.doNewPhysics:
            tag += f'_Zprime_{self.MZprime}_Gamma_{self.GammaZprime}_mode_{decays[self.decayMode]}_xsectFrac_{self.MZprimeHadXsectFraction:1.2f}'
        return tag
    
    def Print(self):
        print(f'Inelasticity      : {self.Inelasticity}')
        print(f'sigmaInelasticity : {self.sigmaInelasticity}')
        print(f'PionsConst        : {self.PionsConst}')
        print(f'sigmaPionConst    : {self.sigmaPionConst}')
        print(f'doNewPhysics      : {self.doNewPhysics}')
        if self.doNewPhysics:
            print(f'MZprimeHadXsectFraction : {self.MZprimeHadXsectFraction}')
            print(f'MZprime                 : {self.MZprime} GeV')
            print(f'GammaZprime             : {self.GammaZprime} GeV')
            print(f'decayMode               : {decays[self.decayMode]}')
            print(f'Ethr                    : 10^{log10(pow(self.MZprime,2)/2)+9:.1f} eV')
        
##########################################

