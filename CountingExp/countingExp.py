#!/snap/bin/pyroot
# was: #!/usr/bin/python3
# Pá 26. ledna 2024, 22:47:33 CET

#from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt
import string

cans = []
stuff = []

# make several 1-bin data-like histos
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
        hd.GetXaxis().SetLabelOffset(-10)
        hd.GetYaxis().SetLabelOffset(-10)
        hds.append(hd)
    return hds

##########################################
def MakeHistos(name, vals, col, x1 = -0.5, x2 = 0.5):
    hs = []
    for i in range(0, len(vals)):
        tag = f'_{i}'
        h = ROOT.TH1D(name + tag, name + tag, 1, x1, x2)
        h.Reset()
        h.SetBinContent(1, vals[i])
        h.SetBinError(1, sqrt(vals[i]))
        h.SetFillColor(col)
        h.SetLineColor(h.GetFillColor())
        h.SetFillStyle(1111)
        h.SetStats(0)
        h.Scale(1.)
        hs.append(h)
    return hs
    


##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):

    rnd = ROOT.TRandom3(1234)
    
    nb = 5
    x1 = 0
    x2 = nb
    nd = 117

    # data
    hDs = MakeHds(nb, nd, rnd)

    # background
    vals = [nd/5, 0.95*nd, 1.1*nd, nd*1.1, nd/2]
    hBs = MakeHistos('bg', vals, ROOT.kBlue-6)

    # s:
    vals = [nd/10, nd/10, 0.3*nd, nd/10, nd/2.5]
    hSs = MakeHistos('s', vals, ROOT.kRed-9)

    canname = 'countingExp'
    cw = 200
    ch = 500
    can = ROOT.TCanvas(canname, canname, 1, 1, nb*cw, ch)
    can.Divide(nb, 1)
    cans.append(can)
    ROOT.gStyle.SetOptTitle(0)

    
    hstacks = []
    texs = []
    j = 0
    labels = string.ascii_lowercase
    for hd, hb, hs in zip(hDs, hBs, hSs):
        j = j+1
        name = f'stack_{j-1}'
        hstack = ROOT.THStack(name, name)
        hstack.Add(hb)
        hstack.Add(hs)
        can.cd(j)
        hd.Draw('e1 x0')
        hstack.Draw('same hist')
        hd.Draw('same e1 x0')
        tex = ROOT.TLatex(0.43, 0.035, '({})'.format(labels[j-1]))
        tex.SetNDC()
        tex.SetTextSize(0.15)
        tex.Draw()
        texs.append(tex)
        ROOT.gPad.Update()
        ROOT.gPad.RedrawAxis()
        #ROOT.gPad.SetTicks()
        hstacks.append(hstack)

    can.Print(can.GetName() + '.png')
    can.Print(can.GetName() + '.pdf')
    
    stuff.append([hDs, hBs, hSs, hstacks, can, texs])
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

