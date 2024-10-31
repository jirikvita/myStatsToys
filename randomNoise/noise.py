#!/usr/bin/python
# was: #!/snap/bin/pyroot
# was: #!/usr/bin/python3
# Čt 31. října 2024, 11:43:44 CET

import ROOT
from math import sqrt, pow, log, exp, factorial
import os, sys, getopt



from numpy import random

# see $PYTHONPATH
from mystyle import *

cans = []


stuff = []
##########################################

def getRandomHisto(name, title, nbins, xmin, xmax, c, A):
    h = ROOT.TH1D(name, title, nbins, xmin, xmax)
    for i in range(nbins):
        h.SetBinContent(i+1, c+A*random.uniform(-1, 1))
    return h

##########################################

def addRandomGauss(h, mu, sigma, A):
    N = h.GetNbinsX()
    for i in range(N):
        x = h.GetBinCenter(i+1)
        val = A*exp(-(x - mu)**2 / (2*sigma**2)) 
        #print(val)
        cont = h.GetBinContent(i+1)
        h.SetBinContent(i+1, cont + val) 
    h.Scale(1.)

##########################################

def mypoisson(k, mu):
    return mu**k * exp(-mu) / factorial(k)

##########################################
##########################################
##########################################

# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    #if len(sys.argv) > 1:
    #  foo = sys.argv[1]

   
    SetDarkStyle()


    # random noise and multi gauss transient

    canname = 'can_transient'
    can = ROOT.TCanvas(canname, canname, 0, 0, 1000, 800)
    cans.append(can)

    N = 2000
    c = 10.
    A = 0.3
    h1 = getRandomHisto('h1', ';time bin;Amplitude', N, 0, N, c, A)
    
    mus= [N/10, N/6, N/4]
    sigmas = [20, 30, 50]
    As = [-5, -1.3, -0.5]
    for mu, sigma, a in zip(mus, sigmas, As):
        addRandomGauss(h1, mu, sigma, a)
    
    h1.SetLineColor(ROOT.kMagenta)
    
    h1.SetMinimum(0)
    h1.SetMaximum(c + 5*A)
    
    h1.Draw('hist')   
    makeWhiteAxes(h1)
    
    stuff.append(h1)

    # pedestal and p.e. peaks

    canname = 'can_pe'
    can = ROOT.TCanvas(canname, canname, 200, 200, 1000, 800)
    cans.append(can)

    # noise:
    c = 10.
    A = 5.
    
    # poissons:
    PoissonMuNpe = 1.1
    Q0 = 1.1
    sigma0 = 0.40*Q0
    # 1pe center in charge 
    Nevts = 1000
    # number of bins and max range
    Qmax = 10*Q0
    nbins = 500
    h0 = getRandomHisto('h0', ';Charge;Events', nbins, 0, Qmax, c, A)
    
    mus= [ i*Q0 for i in range(0,10)]
    As = [Nevts, Nevts*mypoisson(1, PoissonMuNpe), Nevts*mypoisson(2, PoissonMuNpe), Nevts*mypoisson(3, PoissonMuNpe)]
    sigmas = [sigma0/2]
    sigmas.extend([sigma0 for i in range(len(As)-1)])
    for mu, sigma, a in zip(mus, sigmas, As):
        print(mu, sigma, a)
        addRandomGauss(h0, mu, sigma, a)
    
    h0.SetLineColor(ROOT.kCyan)
    h0.SetLineWidth(2)
    
    #h0.SetMinimum(0)
    #h0.SetMaximum(c + 5*A)
    
    h0.Draw('hist')   
    makeWhiteAxes(h0)

    stuff.append(h0)


    for can in cans:
        can.Print(can.GetName() + '.pdf')
        can.Print(can.GetName() + '.png')
        ROOT.gPad.Update()

    ROOT.gApplication.Run()
    return

###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################

