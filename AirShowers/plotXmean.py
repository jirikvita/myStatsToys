#!/usr/bin/python

#jk 6.9.2024
import ROOT
from math import pow, log10

Es = [ int(pow(10,n)) for n in range(2,6)]
print(Es)

fs = []
hs = []

gr = ROOT.TGraphErrors()
hname = 'h1Nx'
ip = 0
for E in Es:
    fname = f'histos_pi_E{E}GeV.root'
    infile = ROOT.TFile(fname, 'read')
    fs.append(infile)
    h = infile.Get(hname)
    try:
        mean = h.GetMean()
        err = h.GetMeanError()
        print(mean)
        hs.append(h)
        gr.SetPoint(ip, log10(E) + 9, mean)
        gr.SetPointError(ip, 0., err)
        ip = ip+1
    except:
        print(f'Error getting {hname} from {fname}')


canname = 'CmpXmean'
can = ROOT.TCanvas(canname, canname, 0, 0, 1000, 800)

h2 = ROOT.TH2D('tmp', ';x[g/cm^{2}];Events', 100, 0, 900, 100, 0, 10000)
h2.SetStats()
h2.Draw()
opt = ' same'
for h in hs:
    h.Draw('hist plc' + opt)
    opt = ' same'
ROOT.gPad.BuildLegend()
ROOT.gPad.Update()

canname = 'GrXmean'
gcan = ROOT.TCanvas(canname, canname, 0, 0, 1000, 800)
gr.SetMarkerColor(ROOT.kBlack)
gr.SetMarkerSize(1)
gr.SetMarkerStyle(20)
gr.SetLineColor(ROOT.kBlack)
gr.SetLineWidth(1)
gr.SetLineStyle(1)
gr.GetXaxis().SetTitle('log_{10}E(eV)')
gr.GetYaxis().SetTitle('X_{mean}^{N} [g/cm^{2}]')
gr.GetYaxis().SetRangeUser(0, 900)
gr.Draw('APL')
ROOT.gPad.Update()

ROOT.gApplication.Run()
    
