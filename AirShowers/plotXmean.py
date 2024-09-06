#!/usr/bin/python

#jk 6.9.2024
import ROOT
from math import pow, log10, pow, sqrt


########################################

def getMaxima(hs):
    maxy = -1
    for h in hs:
        val = h.GetMaximum()
        if val > maxy:
            maxy = 1.*val
    return maxy

########################################

ROOT.gStyle.SetPalette(1)

cans = []
stuff = []

########################################

Es = [ int(pow(10,n)) for n in range(2,7)]
print(Es)

Fs = []
Hs = {}

gr = ROOT.TGraphErrors()
hbasename = 'h1Nx'

Means = []
for E in Es:
    fname = f'histos_pi_E{E}GeV.root'
    infile = ROOT.TFile(fname, 'read')
    Fs.append(infile)
    Hs[E] = []
    meansum = 0
    meanSqSum = 0
    np = 0
    for i in range(0,10):
        hname = hbasename + f'_{i}'
        h = infile.Get(hname)
        try:
            mean = h.GetBinCenter(h.GetMaximumBin()) #h.GetMean()
            err = h.GetMeanError()
            #print(mean)
            Hs[E].append(h)
            np = np+1
            meansum = meansum + mean
            meanSqSum = meanSqSum + pow(mean,2)
        except:
            print(f'Error getting {hname} from {fname}')
    if np > 1 and meansum > 0:
        meanMean = meansum / np
        meanErrSq = (pow(meanMean,2) - meanSqSum / (np-1) )
        print(pow(meanMean,2), meanSqSum, meanSqSum )
        meanErr = 0.
        if meanErrSq > 0:
            meanErr = sqrt(meanErrSq)
        Means.append([E, meanMean, meanErr])

ip = 0
for meanData in Means:
    E = meanData[0]
    mean = meanData[1]
    meanErr = meanData[2]
    gr.SetPoint(ip, log10(E) + 9, mean)
    gr.SetPointError(ip, 0., meanErr)
    ip = ip+1

H2s = []
canname = f'CmpXmean_{E}'
can = ROOT.TCanvas(canname, canname, 0, 0, 1000, 800)
cans.append(can)
can.Divide(2,3)
ie = 0
for E,hs in Hs.items():
    can.cd(1+ie)
    ie = ie + 1
    ymax = getMaxima(hs)*1.1
    h2 = ROOT.TH2D(f'tmp_{E}', ';x[g/cm^{2}];Events', 100, 0, 1500, 100, 0, ymax)
    h2.SetStats(0)
    h2.Draw()
    H2s.append(h2)
    
    opt = ' same'
    for h in hs:
        h.SetLineWidth(2)
        h.SetStats(0)
        h.Draw('hist plc' + opt)
        opt = ' same'
    #ROOT.gPad.BuildLegend()
ROOT.gPad.Update()

canname = 'GrXmean'
gcan = ROOT.TCanvas(canname, canname, 500, 500, 800, 600)
gr.SetMarkerColor(ROOT.kBlack)
gr.SetMarkerSize(1)
gr.SetMarkerStyle(20)
gr.SetLineColor(ROOT.kBlack)
gr.SetLineWidth(1)
gr.SetLineStyle(1)
gr.GetXaxis().SetTitle('log_{10}E(eV)')
gr.GetYaxis().SetTitle('X_{max}^{N} [g/cm^{2}]')
gr.GetYaxis().SetRangeUser(0, 900)
gr.Draw('APL')

ROOT.gPad.Update()

can.Print(can.GetName() + '.png')
can.Print(can.GetName() + '.pdf')

gcan.Print(gcan.GetName() + '.png')
gcan.Print(gcan.GetName() + '.pdf')

stuff.append([Hs, Fs])

ROOT.gApplication.Run()
    
