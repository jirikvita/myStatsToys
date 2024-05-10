#!/snap/bin/pyroot
# /usr/bin/python3
# Po 19. února 2024, 09:33:36 CET

import ROOT

from math import sqrt, pow, log, exp, pi
import os, sys, getopt
from random import uniform

#from matplotlib import pyplot as plt
#import matplotlib.patches as patches


stuff = []
##########################################
def getPiGuesstimate(Nevts, sthr, s, storePoints = False):
    Nin = 0
    Nall = 0
    xsin = []
    ysin = []
    xsout = []
    ysout = []
    for i in range(0, Nevts):
        x = uniform(0,1)
        y = uniform(0,1)
        if x*y*s <= sthr:
            Nin = Nin + 1
            if storePoints:
                xsin.append(x)
                ysin.append(y)
        else:
            if storePoints:
                xsout.append(x)
                ysout.append(y)

        Nall = Nall + 1
    return xsin, ysin, xsout, ysout

##########################################
def PlotPoint(xs, ys, sthr, s):
    fun = ROOT.TF1('fun', '[0]/x', 0, 1)
    fun.SetParameters(sthr/s)
    nb = 100
    h = ROOT.TH2D('tmp', ';x_{1};x_{2}', nb, 0, 1, nb, 0, 1)
    h.SetStats(0)

    canname = 'FactorizationTheorem'
    can = ROOT.TCanvas(canname, canname, 0, 0, 820, 800)
    h.Draw()

    fun.SetNpx(300)
    #fun.SetFillStyle(1111)
    col = ROOT.kGreen+2
    fun.SetLineColor(col)
    #fun.SetFillColorAlpha(col, 0.7)
    fun.Draw('same')

    ps = []
    for x,y in zip(xs,ys):
        p = ROOT.TMarker(x,y, 20)
        p.SetMarkerSize(0.4)
        p.SetMarkerColor(ROOT.kGreen+2)
        p.Draw()
        ps.append(p)
    
    return can, fun, h, ps
##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
   
    Xs = []
    Ys = []

    Nevt = 5000

    # tt, LHC
    #sthr = sqrt(2*172.5)
    #s = sqrt(13.6e3)

    # tt, Tevatron
    #sthr = sqrt(2*172.5)
    #s = sqrt(1.96e3)

    # ttH
    sthr = sqrt(2*172.5 + 125.)
    s = sqrt(13.6e3)

    storePoints = True
    
    xsin, ysin, xsout, ysout = getPiGuesstimate(Nevt, sthr, s, storePoints)
    can, fun, h, ps = PlotPoint(xsout, ysout, sthr, s)
    stuff.append([can, fun, h, ps])

    ROOT.gPad.Update()
    #fr = ROOT.gPad.GetFrame()
    ROOT.gPad.RedrawAxis()

    can.Print(can.GetName() + '.pdf')
    can.Print(can.GetName() + '.png')
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

