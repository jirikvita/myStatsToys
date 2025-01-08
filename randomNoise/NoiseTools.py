#!/usr/bin/python

import ROOT

from numpy import random
# see $PYTHONPATH
from mystyle import *

from math import sqrt, pow, log, exp, factorial, sin, cos

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


def makeFFT(h0, canname):
    h0fft_re = h0.Clone('fft_re')
    h0.FFT(h0fft_re, 'RE')
    h0fft_im = h0.Clone('fft_im')
    h0.FFT(h0fft_im, 'IM')

    canno = ROOT.TCanvas(canname, canname, 200, 200, 1200, 600)
    canno.Divide(3,1)
    cans.append(canno)
    
    canno.cd(1)
    h0.SetLineColor(ROOT.kRed)
    h0.SetStats(0)
    h0.Draw('hist')
    makeWhiteAxes(h0)

    canno.cd(2)
    h0fft_re.SetLineColor(ROOT.kYellow)
    h0fft_re.SetStats(0)
    h0fft_re.SetTitle('Re;bin;Re')
    #h0fft_re.Rebin(5)
    h0fft_re.Draw('hist')
    makeWhiteAxes(h0fft_re)

    canno.cd(3)
    h0fft_im.SetLineColor(ROOT.kGreen)
    h0fft_im.SetStats(0)
    h0fft_im.SetTitle('Im;bin;Im')
    #h0fft_im.Rebin(5)
    h0fft_im.Draw('hist')
    makeWhiteAxes(h0fft_im)

    return canno, h0fft_re, h0fft_im
