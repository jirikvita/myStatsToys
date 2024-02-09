#!/snap/bin/pyroot
# was: #!/usr/bin/python3
# Pá 26. ledna 2024, 22:47:33 CET

#from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp, factorial
import os, sys, getopt
import string

cans = []
stuff = []

# make several data-like points
# todo: make this vertical lines, not histos!
##########################################
def MakeHds(nb, nd, rnd, x1 = -0.5, x2 = 0.5):
    hds = []
    name = 'data'
    for i in range(0,nb):
        tag = f'_{i}'
        hd = ROOT.TH1D(name + tag, name + tag, 1, x1, x2)
        hd.SetMarkerStyle(20)
        hd.SetMarkerSize(1.8)
        hd.SetLineWidth(2)
        hd.SetBinContent(1, rnd.Poisson(nd))
        hd.SetBinError(1, sqrt(hd.GetBinContent(1)) )
        hd.SetStats(0)
        hd.Scale(1.)
        hd.SetMinimum(0.)
        hd.SetMaximum(1.5*nd)
        #hd.GetXaxis().SetLabelOffset(-10)
        #hd.GetYaxis().SetLabelOffset(-10)
        hds.append(hd)
    return hds

##########################################
def MakePoissonHisto(name, nu, dxi, col, n1 = 0., n2 = 100, plenty = 2, ymax = 0.22):
    h = ROOT.TH1D(name, name + ';k;;', n2*plenty, n1, n2)
    for i in range(0, n2):
        ibin = h.GetXaxis().FindBin(i+1 + dxi)
        h.SetBinContent(ibin, exp(-nu) * pow(nu, i) / factorial(i) )
        h.SetBinError(ibin, 0)
    h.SetFillColor(col)
    h.SetLineColor(h.GetFillColor())
    h.SetFillStyle(1111)
    h.SetStats(0)
    h.Scale(1.)
    h.SetMinimum(0.)
    h.SetMaximum(ymax)
    return(h)
        
    
##########################################
def MakeHistos(name, nus, col, nmax, ddx = 0.1):
    hs = []
    for i in range(0, len(nus)):
        tag = f'_{i}'
        h = MakePoissonHisto(name + tag, nus[i], ddx, col, 0, nmax)
        hs.append(h)
    return hs


##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):

    rnd = ROOT.TRandom3(1234)
    
    nb = 5
    nd = 40
    n2 = int(1.3*nd)
    
    # data
    hDs = MakeHds(nb, nd, rnd)

    # background
    nus = [nd/10, nd/3.5, nd/5, nd/10,
           #10
           ]
    hBs = MakeHistos('bg', nus, ROOT.kBlue-6, n2, -0.1)

    # s+b:
    nus = [nd/5, nd/2, nd*0.65, 0.9*nd,
           #18
    ]
    hSs = MakeHistos('sb', nus, ROOT.kRed-9, n2, +0.1)

    canname = 'poissonH0H1'
    cw = 400
    ch = 300
    can = ROOT.TCanvas(canname, canname, 1, 1, cw*2, ch*2)
    can.Divide(2,2)
    cans.append(can)
    ROOT.gStyle.SetOptTitle(0)
    
    texs = []
    j = 0
    labels = string.ascii_lowercase
    for hd, hb, hs in zip(hDs, hBs, hSs):
        j = j+1
        name = f'stack_{j-1}'
        can.cd(j)
        #hd.Draw('e1 x0')
        hb.Draw('hist')
        hs.Draw('hist same')
        
        #hd.Draw('same e1 x0')
        tex = ROOT.TLatex(0.45, 0.028, '({})'.format(labels[j-1]))
        tex.SetNDC()
        tex.SetTextSize(0.06)
        tex.Draw()
        texs.append(tex)
        ROOT.gPad.Update()
        ROOT.gPad.RedrawAxis()
        #ROOT.gPad.SetTicks()

    can.Print(can.GetName() + '.png')
    can.Print(can.GetName() + '.pdf')
    
    stuff.append([hDs, hBs, hSs, can, texs])
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

