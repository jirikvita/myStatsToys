#!/snap/bin/pyroot
# was: #!/usr/bin/python3
# So 10. února 2024, 00:03:50 CET

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt
import random

cans = []
stuff = []

##########################################
def main(argv):


    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    
    Nevt = 1000
    x1, x2, nb = 0., 250., 20   
    
    fun = ROOT.TF1("fun", "[0]*x*exp(-[1]*x)", x1, x2)
    fun.SetParameters(10, 0.022)
    
    efffun = ROOT.TF1("efffun", "1. - exp(-[0]*x)", x1, x2)
    efffun.SetParameter(0, 0.04)
    
    name = 'htot'
    title = name + ';x;n;'
    htot = ROOT.TH1D(name, title, nb, x1, x2)
    htot.SetFillColorAlpha(ROOT.kBlue, 0.4)
    htot.SetFillStyle(1111)
    
    name = 'hpassed'
    title = name + ';x;passed;'
    hpassed = ROOT.TH1D(name, title, nb, x1, x2)
    hpassed.SetFillColorAlpha(ROOT.kRed, 0.4)
    hpassed.SetFillStyle(1111)
    
    for i in range(0, Nevt):
        x = fun.GetRandom()
        yf = efffun.Eval(x)
        htot.Fill(x)
        y = random.uniform(0,1)
        if y < yf:
            hpassed.Fill(x)

    heff = ROOT.TEfficiency(hpassed, htot)
    heff.SetMarkerStyle(20)
    heff.SetMarkerSize(1.4)
    heff.SetMarkerColor(ROOT.kBlack)
    heff.SetTitle(';x;#epsilon')
    canname = 'EfficiencyBinomial'
    w = 800
    can = ROOT.TCanvas(canname, canname, 0, 0, 2*w, w)
    can.Divide(2,1)
    cans.append(can)
    can.cd(1)
    htot.Draw('hist')
    hpassed.Draw('hist same')
    
    can.cd(2)
    heff.Draw("e1")
    ROOT.gPad.SetGridy()
    
    can.Update()
    can.Print(can.GetName() + '.png')
    can.Print(can.GetName() + '.pdf')
    
    stuff.append([htot, hpassed, heff])
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

