#!/usr/bin/python
# Út 15. listopadu 2022, 14:04:33 CET

#from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

from FitTools import *

cans = []
stuff = []
##########################################
def main(argv):

    x1,x2 = 0., 100.

    fun = ROOT.TF1('fun', '[0]/(TMath::Sqrt(2*TMath::Pi())*[2])*exp(-(x-[1])^2/(2*[2]^2)) + [3]/(TMath::Sqrt(2*TMath::Pi())*[5])*exp(-(x-[4])^2/(2*[5]^2))', x1, x2)
    f = 0.65
    fun.SetParameters(f, 20, 10, (1.-f), 60, 15)

    hname = 'histo_h'
    nb = 100
    h1 = ROOT.TH1D(hname, hname + ';;Events', nb, x1, x2)

    Nmax = 400 # for drawing lines
    N = 10000
    for i in range(0, N):
        x = fun.GetRandom()
        h1.Fill(x)
    binwidth = (x2-x1) / nb
    h1.Scale(1.)
    
    lines = []
    ymax = h1.GetMaximum()
    ymin = h1.GetMinimum()
    Delta = ymax - ymin
    y0 = ymin - 10*Delta / 100.
    w = Delta/30.
    y1,y2 = y0-w,y0+w
    print(y1,y2)
    for i in range(0, Nmax):
        x = fun.GetRandom()
        line = ROOT.TLine(x, y1, x, y2)
        line.SetLineColor(ROOT.kBlue)
        lines.append(line)
        
    h1.SetMarkerStyle(20)
    h1.SetMarkerSize(1)
    h1.SetMarkerColor(ROOT.kBlack)
    h1.SetLineColor(ROOT.kBlack)
    h1.SetStats(0)

    ROOT.gStyle.SetOptTitle(0)
    cw = 800
    ch = 1000
    canname = 'can'
    can = ROOT.TCanvas(canname, canname, 0, 0, cw, ch)
    cans.append(can)

    allstuff = DrawHistFitResidualsSignif(h1, fun, can)

    signifh = allstuff['signifh']
    signifh.SetTitle(';X [unit]')
    
    pads = allstuff['pads']
    pads[0].cd()
    for line in lines:
        line.Draw()
    
    can.Update()
    can.Print('FitIllustration.png')
    can.Print('FitIllustration.pdf')

    stuff.append(allstuff)
    stuff.append([can, fun, h1, lines])
    
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

