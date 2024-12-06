#!/usr/bin/python
# was: #!/snap/bin/pyroot
# was: #!/usr/bin/python3
# Čt 31. října 2024, 11:43:44 CET

import ROOT
from math import sqrt, pow, log, exp, factorial, sin, cos
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
        val = c+A*random.uniform(-1, 1)
        err = 0.
        if val > 0:
            err = sqrt(val)
        h.SetBinContent(i+1, val)
        h.SetBinError(i+1, err)
        
    return h

##########################################

def addRandomSinGauss(h, mu, sigma, A, phi0, freq):
    N = h.GetNbinsX()
    for i in range(N):
        x = h.GetBinCenter(i+1)
        val = A*exp(-(x - mu)**2 / (2*sigma**2)) * sin(phi0 + x*freq)
        #print(val)
        cont = h.GetBinContent(i+1)
        h.SetBinContent(i+1, cont + val) 
    h.Scale(1.)

def addRandomSin(h, phi0, freq, B):
    N = h.GetNbinsX()
    for i in range(N):
        x = h.GetBinCenter(i+1)
        val = B*sin(phi0 + x*freq)
        #print(val)
        cont = h.GetBinContent(i+1)
        h.SetBinContent(i+1, cont + val) 
    h.Scale(1.)

def addRandomGauss(h, mu, sigma, A):
    N = h.GetNbinsX()
    for i in range(N):
        x = h.GetBinCenter(i+1)
        val = A*exp(-(x - mu)**2 / (2*sigma**2)) 
        #print(val)
        cont = h.GetBinContent(i+1)
        newval = cont + val
        err = h.GetBinError(i+1)
        if newval > 0:
            err = sqrt(newval)
        h.SetBinContent(i+1, newval)
        h.SetBinError(i+1, err)
        
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

    mmu, msigma, phi0, freq, B = 700, 60, 0., 0.1, 0.3
    #addRandomSin(h1, phi0, freq, B)
    # sine modulated by Gauss:
    addRandomSinGauss(h1, mmu, msigma, B, phi0, freq)
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
    h0 = getRandomHisto('h0', ';Charge;Events', nbins, 0, Qmax, c, 3*A)
    
    mus= [ i*Q0 for i in range(0,10)]
    As = [Nevts, Nevts*mypoisson(1, PoissonMuNpe), Nevts*mypoisson(2, PoissonMuNpe), Nevts*mypoisson(3, PoissonMuNpe)]
    sigmas = [sigma0/2]
    sigmas.extend([sigma0 for i in range(len(As)-1)])
    for mu, sigma, a in zip(mus, sigmas, As):
        print(mu, sigma, a)
        addRandomGauss(h0, mu, sigma, a)
    
    h0.SetLineColor(ROOT.kCyan)
    h0.SetLineWidth(2)

    x0 = 1.2
    x1,x2 = 0.7, 2.5
    #x1,x2 = 0.7, 1.5
    sigma = 0.2
    
    fun = ROOT.TF1('fit', '[0]*exp(-(x-[1])^2/(2*[2]^2)) + [3]*exp(-(x-[4])^2/(2*[5]^2))', x1, x2)
    #fun = ROOT.TF1('fit', '[0]*exp(-(x-[1])^2/(2*[2]^2)) + [3]*exp(-(x-[4])^2/(2*[5]^2))', x1, x2)
    jbin = h0.GetXaxis().FindBin(x0)
    ymax = h0.GetBinContent(jbin)
    print(f'paramas: {x1} {x0} {x2} {sigma} {jbin} {ymax:1.3f}')
    fun.SetParameters(ymax, x0, sigma, ymax*2./3., 2*x0, sigma)
    #fun.SetParameters(ymax, x0, sigma)
    #fun.SetParLimits(1, x1, x2)
    fun.SetLineWidth(3)
    
    #h0.SetMinimum(0)
    #h0.SetMaximum(c + 5*A)
    
    h0.Draw('hist e1')
    h0.Fit(fun, '', '', x1, x2)
    fun.Draw('same')

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

