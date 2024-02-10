#!/usr/bin/python
# Út 15. listopadu 2022, 14:04:33 CET

#from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

cans = []
stuff = []

##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    #if len(sys.argv) > 1:
    #  foo = sys.argv[1]

    ### https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    ### https://pymotw.com/2/getopt/
    ### https://docs.python.org/3.1/library/getopt.html
    gBatch = False
    gTag=''
    print(argv[1:])
    try:
        # options that require an argument should be followed by a colon (:).
        opts, args = getopt.getopt(argv[2:], 'hbt:', ['help','batch','tag='])

        print('Got options:')
        print(opts)
        print(args)
    except getopt.GetoptError:
        print('Parsing...')
        print ('Command line argument error!')
        print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]]'.format(argv[0]))
        sys.exit(2)
    for opt,arg in opts:
        print('Processing command line option {} {}'.format(opt,arg))
        if opt == '-h':
            print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]'.format(argv[0]))
            sys.exit()
        elif opt in ("-b", "--batch"):
            gBatch = True
        elif opt in ("-t", "--tag"):
            gTag = arg
            print('OK, using user-defined histograms tag for output pngs {:}'.format(gTag,) )

    if gBatch:
        ROOT.gROOT.SetBatch(1)

    print('*** Settings:')
    print('tag={:}, batch={:}'.format(gTag, gBatch))

    canname = 'can'
    can = ROOT.TCanvas(canname, canname)
    cans.append(can)

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
    h1.Scale(1./N / binwidth)
    
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
        if i < Nmax:
            line = ROOT.TLine(x, y1, x, y2)
            line.SetLineColor(ROOT.kBlue)
            lines.append(line)
        
    h1.SetMarkerStyle(20)
    h1.SetMarkerSize(1)
    h1.SetMarkerColor(ROOT.kBlack)
    h1.SetLineColor(ROOT.kBlack)
    h1.SetStats(0)

    ROOT.gStyle.SetOptTitle(0)

    h1.Draw('e1 x0')

    #h1.Fit(fun)
    for line in lines:
        line.Draw()
    
    
    can.Update()
    can.Print('BinnedUnbinnedIllustration_nofun.png')
    can.Print('BinnedUnbinnedIllustration_nofun.pdf')

    fun.Draw('same')
    can.Update()
    can.Print('BinnedUnbinnedIllustration.png')
    can.Print('BinnedUnbinnedIllustration.pdf')
    
    stuff.append([can, fun, h1, line])
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

