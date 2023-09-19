#!/usr/bin/python3
# Ne 23. října 2022, 10:30:18 CEST

#from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

from numpy import random

cans = []
stuff = []

##########################################

def MakeSequence(n = 1024):
    seq = []
    for i in range(0,n):
        rnd = random.uniform(0, 1)
        seq.append(rnd)
    return seq

##########################################
def AnalyzeSeq(seq, n1 = 1, n2 = 10):
    actual = -1
    n = 0
    name = 'SeqLengthHist'
    title = name + ';n;#'
    h1 = ROOT.TH1D(name, title, n2 - n1, n1, n2)
    for rnd in seq:
        j = 0
        if rnd >= 0.5:
            j = 1
        if actual != 1.*j:
            if n > 0:
                h1.Fill(n)
            n = 1
            actual = 1.*j
        else:
            n = n + 1
    return h1

##########################################

def DrawSeq(can, seq, 
            col0 = ROOT.kBlack, col1 = ROOT.kRed,
            #useBinaryCols = False,
            useBinaryCols = True,
            smallerDelta = 0.,
            #smallerDelta = 0.1,
            #lsz = 2
):
    can.cd()
    can.Range(0,0,1,1)

    marks = []
    root = int(sqrt(len(seq)))
    ddx = 1. / (root)
    ddy = ddx
    x0 = ddx/2.
    y0 = 1. - ddy/2.
    nCol = root
    R = (0.5 - smallerDelta)*(1. - 2*ddx) / root
    print(R)
    
    
    for j in range(0,len(seq)):
        rnd = seq[j]
        i = 0
        if rnd >= 0.5:
            i = 1
        x = x0 + ddx*(j % nCol)
        y = y0 - ddy*(j // nCol)
        #print('{:1.2f},{:1.2f}'.format(x,y))
        #if j >= nCol*nRow:
        #    break
        mark = ROOT.TEllipse(x, y, R, R)
        mark.SetFillStyle(1001)
        col = col1
        if useBinaryCols:
            if i == 0:
                col = col0
        else:
            tcol = ROOT.TColor()
            col = tcol.GetColorPalette(int(tcol.GetNumberOfColors()*rnd))
        mark.SetFillColor(col)
        mark.SetLineColor(col)
        #mark.SetLineWidth(lsz)
        #print('drawing...')
        mark.Draw()
        marks.append(mark)
    return marks


##########################################

def StatSnalyzeRepetitions():
    pass

##########################################

def DrawBoxesAroundRepetitions():
    pass

        
##########################################

# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    #if len(sys.argv) > 1:
    #  foo = sys.argv[1]

    ROOT.gStyle.SetPalette(1)
    #ROOT.gStyle.SetPalette(ROOT.kTemperatureMap)
    #ROOT.gStyle.SetPalette(ROOT.kDarkBodyRadiator)
    #ROOT.gStyle.SetPalette(ROOT.kBlueRedYellow)
    
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

    N = 1024
    canname = 'RndSeq_{}'.format(N)
    #cw,ch = 200,200
    cw,ch = 1000,1000
    can = ROOT.TCanvas(canname, canname, 0, 0, cw, ch)
    cans.append(can)
    
  
    seq = MakeSequence(N)
    #print(seq)
    marks = DrawSeq(can, seq)

    can.Print(can.GetName() + '.png')
    #can.Print(can.GetName() + '.pdf')

    h1 = AnalyzeSeq(seq)
    ROOT.gStyle.SetOptTitle(0)
    h1.SetFillColor(ROOT.kCyan)
    h1.SetMarkerSize(1)
    h1.SetMarkerStyle(24)
    

    canname = 'SeqCounts'
    can = ROOT.TCanvas(canname, canname, 200, 200, 1000, 1000)
    cans.append(can)
    can.cd()
    h1.SetStats(0)
    h1.Draw('e1')
    h1.Draw('hist same')
    h1.Draw('e1 same')
    can.RedrawAxis()
    
    txt = ROOT.TLatex(0.72, 0.84, '#mu = {:1.2f}'.format(h1.GetMean()))
    txt.SetNDC()
    txt.Draw()
    can.Print(can.GetName() + '.png')
    #can.Print(can.GetName() + '.pdf')
    
    stuff.append(seq)
    stuff.append(marks)
    stuff.append([h1, txt])

    if not gBatch:
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

