#!/usr/bin/python
import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt
from mystyle import *

cans = []
stuff = []

def main(argv):
    SetDarkStyle()
    canname = 'can'
    can = ROOT.TCanvas(canname, canname, 0, 0, 1000, 1000)
    cans.append(can)

    #pows = [3, 2, 1, 0.5, 0.25, 0.1, 0.01, 0]
    pows = [0, 0.01, 0.1, 0.25, 0.5, 1, 2, 3]
    funs = []
    formula = 'x^[0]'
    x1, x2 = 0., 1.
    leg = ROOT.TLegend(0.75, 0.12, 0.88, 0.45)
    makeDarkLegend(leg)

    cols = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kCyan, 
            ROOT.kMagenta, ROOT.kYellow, ROOT.kTeal, ROOT.kSpring]

    for c,q in zip(cols,pows):
        fname = f'pow_{q}'
        fun = ROOT.TF1(fname, formula, x1, x2)  
        fun.SetParameter(0, q)
        fun.SetLineColor(c)
        fun.SetLineWidth(3)
        fun.SetNpx(1000)
        funs.append(fun)
        
    opt = ''
    for q,fun in zip(pows,funs):
        fun.Draw(opt)# + 'plc')
        fun.GetXaxis().SetTitle('x')
        fun.GetYaxis().SetRangeUser(0., 1.05)
        opt = 'same'
    funs[0].Draw('same')
    
    #for i in range(len(funs)-1,-1,-1):
    for i in range(len(funs)):
        q = pows[i]
        leg.AddEntry(funs[i], 'x^{' + f'{q}' + '}', 'L')

    makeWhiteAxes(funs[0])
    #leg = ROOT.gPad.BuildLegend()
    leg.Draw()
    ROOT.gPad.SetGridx(1)
    ROOT.gPad.SetGridy(1)
    txt = ROOT.TLatex(0.25, 0.92, 'Na nultou su jednicka!')
    
    
    
    txt.SetTextColor(ROOT.kWhite)
    txt.SetNDC()
    #txt.Draw()
    
    stuff.append([leg, txt])
  
    ROOT.gStyle.SetOptTitle(0)

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

