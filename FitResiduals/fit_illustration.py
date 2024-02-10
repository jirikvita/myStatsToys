#!/usr/bin/python
# Út 15. listopadu 2022, 14:04:33 CET

#from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

from xSectTools import *

from Tools import *


cans = []
stuff = []

##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
   

    gyratioMin, gyratioMax = 0., 2.
     
    x1,x2 = 0., 100.

    fun = ROOT.TF1('fun', '[0]/(TMath::Sqrt(2*TMath::Pi())*[2])*exp(-(x-[1])^2/(2*[2]^2)) + [3]/(TMath::Sqrt(2*TMath::Pi())*[5])*exp(-(x-[4])^2/(2*[5]^2))', x1, x2)
    f = 0.65
    fun.SetParameters(f, 20, 10,
                      (1.-f), 60, 15)

    hname = 'histo_h'
    nb = 100
    h1 = ROOT.TH1D(hname, hname, nb, x1, x2)

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


    # DRAW
    
    ROOT.gStyle.SetOptTitle(0)
    cw = 800
    ch = 1000
    canname = 'can'
    can = ROOT.TCanvas(canname, canname, 0, 0, cw, ch)
    cans.append(can)
    #spad1,spad2,spad_inset = MakePadsStack(can, 'centre', 0.40, 0., 0., 0.)
    pads, inset = MakeMultiSubPads(can,  [0.60, 0.20, 0.20], 0.0,0.07, 0.4, 0.15)
    pads[0].cd()
    
    h1.Draw('e1 x0')

    for line in lines:
        line.Draw()
    
    h1.Fit(fun, '', '0')
    fun.Draw('same')

    # ratio
    pads[1].cd()
    ratio = MakeFitRatioHisto(h1, fun, 'ratio')
    delta = 0.33
    y1 = 1. - delta
    y2 = 1. + delta
    ratio.SetMinimum(y1)
    ratio.SetMaximum(y2)
    ratio.GetXaxis().SetLabelSize(0.12)
    ratio.GetYaxis().SetLabelSize(0.12)
    ratio.GetYaxis().SetTitle('data / fit ')
    ratio.GetYaxis().SetTitleOffset(0.35)
    ratio.GetYaxis().SetTitleSize(0.12)

    ratio.Draw('e1x0')
    line0 = ROOT.TLine(x1, 1., x2, 1.)
    line0.SetLineColor(ROOT.kRed)
    line0.SetLineWidth(2)
    line0.SetLineStyle(2)
    line0.Draw() 
    upHelpHisto = ROOT.TH2D(h1.GetName() + '_upHelp', '',
                            h1.GetXaxis().GetNbins(), x1, x2,
                            100, y1, y2)
    
    sarrowsUp = DrawArrowForPointsOutsideYAxisRange(ratio, upHelpHisto, x1, x2)
    stuff.append(sarrowsUp)

    
    # significance

    pads[2].cd()
    sy1, sy2 = -3, 3
    signifh, ratioScaleHisto, pullh, slines = DrawFitSignificance(fun, h1, x1, x2, sy1, sy2, stuff)
    signifh.SetTitle(';X [unit]')
    signifh.GetXaxis().SetTitleSize(0.12)
    signifh.GetYaxis().SetTitle('Data-fit signif.')
    signifh.GetYaxis().SetTitleOffset(0.35)
    signifh.GetYaxis().SetTitleSize(0.12)

    #signifh.GetYaxis().SetLabelSize(0.12)

    signifh.Draw("hist")
    for sline in slines:
        sline.Draw()

    # now go back to the upper histogram
    # and draw the histogram of fit residuals or pulls
    pads[0].cd()
    inset.Draw()
    inset.cd()
    # for debug
    #inset.SetFillColor(ROOT.kTeal)
    pullh.SetLineWidth(2)
    #pullh.SetStats(0)
    pullh.SetName('pull')
    pullh.GetXaxis().SetTitleSize(0.06)
    pullh.GetYaxis().SetTitleSize(0.06)
    pullh.GetXaxis().SetTitleOffset(0.64)
    pullh.GetYaxis().SetTitleOffset(0.64)
    pullh.Draw()
    adjustStats(pullh)
    
    can.Update()
    can.Print('FitIllustration.png')
    can.Print('FitIllustration.pdf')
    
    stuff.append([can, fun, h1, line, signifh, ratioScaleHisto, sarrowsUp, line0])
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

