#!/usr/bin/python

#jk 6.9.2024
import ROOT
from math import pow, log10, pow, sqrt

import os, sys

from utils import *
from consts import *

########################################

def getMaxima(hs):
    maxy = -1
    for h in hs:
        val = h.GetMaximum()
        if val > maxy:
            maxy = 1.*val
    return maxy


cans = []
stuff = []

########################################

def AddToHeatMap(h2, h):
    for ibin in range(1, h.GetXaxis().GetNbins()+1):
        x = h.GetBinCenter(ibin)
        y = h.GetBinContent(ibin)
        h2.Fill(x,y)

########################################
########################################
########################################

def main(argv):

    SetMyStyle()
    Rebin = 2

    Es = [ int(pow(10,n)) for n in range(2,7)]
    #Es.append(250000)

    print(Es)

    Fs = []
    Hs = {}

    gr = ROOT.TGraphErrors()
    hbasename = 'h1Nx'

    Means = []
    for E in Es:
        fname = f'root/histos_p_E{E}GeV.root'
        infile = None
        try:
            infile = ROOT.TFile(fname, 'read')
        except:
            continue
        Fs.append(infile)
        Hs[E] = []
        means = []
        for i in range(0,502):
            hname = hbasename + f'_{i}'
            h = infile.Get(hname)
            try:
                mean = h.GetBinCenter(h.GetMaximumBin()) #h.GetMean()
                err = h.GetMeanError()
                means.append(mean)
                #print(mean)
                h.Rebin(Rebin)
                if E < 10e3:
                    h.Rebin(2)
                Hs[E].append(h)
            except:
                print(f'Error getting {hname} from {fname}')

        meanSqSum = 0
        np = len(means)
        meanMean = sum(means) / np
        for i in range(0, len(means)):
            meanSqSum = pow(means[i] - meanMean, 2)

        meanErr = 0.
        if np > 1 and meanSqSum > 0:
            meanErr = sqrt(meanSqSum / (np - 1))
            Means.append([E, meanMean, meanErr])

    ip = 0
    print('Got following lengths:')
    for E in Hs:
        print(f'{E}: {len(Hs[E])}')
    for meanData in Means:
        E = meanData[0]
        mean = meanData[1]
        meanErr = meanData[2]
        gr.SetPoint(ip, log10(E) + 9, mean)
        gr.SetPointError(ip, 0., meanErr)
        ip = ip+1

    H2s = []
    Hsums = []
    canname = f'CmpXmean'
    can = ROOT.TCanvas(canname, canname, 0, 0, 1000, 1200)
    cans.append(can)
    can.Divide(2,3)

    canname = f'SumXmean'
    sumcan = ROOT.TCanvas(canname, canname, 600, 0, 1000, 1200)
    cans.append(sumcan)
    sumcan.Divide(2,3)

    ie = 0
    txts = []
    for E,hs in Hs.items():
        can.cd(1+ie)
        ymax = getMaxima(hs)*1.1
        h2 = ROOT.TH2D(f'tmp_{E}', ';x[g/cm^{2}];Particles (e/#mu)', 100, 40, 4000, 100, 0, ymax)
        h2.Draw()
        makeWhiteAxes(h2)
        H2s.append(h2)

        h2sum = ROOT.TH2D(f'hsum_{E}', ';x[g/cm^{2}];Particles (e/#mu)', 40, 0, 4000, 25, 0, ymax)
        makeWhiteAxes(h2sum)
        Hsums.append(h2sum)

        txt = ROOT.TLatex(0.65, 0.8, f'E={E/1000} TeV')
        txt.SetTextColor(ROOT.kWhite)
        txt.SetNDC()
        txt.Draw()
        txts.append(txt)
        opt = ' same'
        for h in hs:
            h.SetLineWidth(1)
            h.SetStats(0)
            h.Draw('hist plc' + opt)
            opt = ' same'
            AddToHeatMap(h2sum, h)
        #ROOT.gPad.BuildLegend()
        ROOT.gPad.RedrawAxis()
        #ROOT.gPad.SetGridx(1)
        #ROOT.gPad.SetGridy(1)
        ROOT.gPad.Update()

        sumcan.cd(1+ie)
        y1 = 1.5*h2sum.GetYaxis().GetBinWidth(1)
        h2sum.GetYaxis().SetRangeUser(y1, h2sum.GetYaxis().GetXmax())
        h2sum.Draw('colz')
        ROOT.gPad.Update()

        ie = ie + 1
        #

    canname = 'GrXmean'
    gcan = ROOT.TCanvas(canname, canname, 500, 500, 800, 600)
    makeGrStyle(gr)
    gr.GetXaxis().SetTitle('log_{10}E(eV)')
    gr.GetYaxis().SetTitle('X_{max}^{N} [g/cm^{2}]')
    gr.GetYaxis().SetRangeUser(0, 1000)
    gr.Draw('APL')
    fun = ROOT.TF1("fit", "[0] + [1]*x", 12., 20.)
    fun.SetParameters(500, 0.1)
    fun.SetLineStyle(2)
    fun.SetLineWidth(1)
    gr.Fit('fit')
    predict17 = fun.Eval(17.)
    print('Fit extrapolation to 10^17 eV: ', predict17)
    gr.GetYaxis().SetAxisColor(ROOT.kWhite)
    gr.GetYaxis().SetLabelColor(ROOT.kWhite)
    gr.GetYaxis().SetTitleColor(ROOT.kWhite)


    ROOT.gPad.SetGridx(1)
    ROOT.gPad.SetGridy(1)
    ROOT.gPad.Update()


    ########################
    # print

    can.Print(can.GetName() + '.png')
    can.Print(can.GetName() + '.pdf')

    gcan.Print(gcan.GetName() + '.png')
    gcan.Print(gcan.GetName() + '.pdf')

    stuff.append([Hs, Fs])

    ROOT.gApplication.Run()


###########################################################
###########################################################
###########################################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)

###########################################################
###########################################################
###########################################################
