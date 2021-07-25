#!/usr/bin/python

import ROOT
from math import *

def DivideByBinWidth(histo):
    for i in range(0, histo.GetNbinsX()):
        val = histo.GetBinContent(i+1)
        err = histo.GetBinError(i+1)
        width =  histo.GetBinWidth(i+1)
        if val > 0:
            histo.SetBinContent(i+1, val/width)
            histo.SetBinError(i+1, err/width)
    histo.Scale(1.)


ROOT.gStyle.SetOptTitle(0)
#ROOT.gStyle.SetOptStat(1001111)
ROOT.gStyle.SetOptFit(1)

nbins = [6, 10, 100, 1000, 10000]

hist = []
xmin = -3
xmax = 3
Nevt = 400
cans = []
cw = 1000
ch = 800
funs = []

formula = '[0]/(sqrt(2*TMath::Pi())*[2]) * exp(-(x-[1])^2/(2*[2]^2))'
gaus = ROOT.TF1('Gauss', formula, xmin, xmax)
mu=0.
sigma=1.
gaus.SetParameters(Nevt , mu, sigma)
print 'Integral of the Gauss: %f' % (gaus.Integral(xmin, xmax))

legs = []

for nb in nbins:
    i = nbins.index(nb)
    name = 'Gaus_bins_%i' % (nb,)
    title = name.replace('_', ' ')
    histo = ROOT.TH1D(name, title, nb, xmin, xmax)
    histo.FillRandom('Gauss', Nevt)
    DivideByBinWidth(histo)
    # histo.SetMaximum(3*histo.GetMaximum() * (xmax-xmin) / histo.GetBinWidth(histo.GetNbinsX()/2))

    canname = 'can_' + name
    can = ROOT.TCanvas(canname, canname, i*100, i*100, cw,  ch )
    cans.append(can)
    can.cd()

    
    fun = ROOT.TF1('Fun_%i' % (i,), formula, xmin, xmax)
    fun.SetParameters(histo.GetEntries(), histo.GetMean(), histo.GetRMS())
    fun.SetParName(0, 'A')
    fun.SetParName(1, '#mu')
    fun.SetParName(2, '#sigma')
    fun.SetLineStyle(2)
    histo.Fit(fun, '0')
    print 'Integral of the fitted Gauss: %f' % (fun.Integral(xmin, xmax))

    hist.append(histo)
    print 'Histogram entries: %f' % (histo.GetEntries(), )

    histo.Draw()
    gaus.DrawCopy('same')
    fun.Draw('same')

    leg = ROOT.TLegend(0.12, 0.7, 0.38, 0.88)
    legs.append(leg)
    leg.AddEntry(gaus, 'Generating function', 'L')
    leg.AddEntry(fun, 'Fit function', 'L')
    leg.SetBorderSize(0)
    leg.SetFillColor(ROOT.kWhite)
    leg.Draw()

    can.Print(can.GetName() + '.png')
    can.Print(can.GetName() + '.pdf')
    funs.append(fun)

    
ROOT.gApplication.Run()
