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

    ROOT.gStyle.SetPalette(ROOT.kTemperatureMap)
    ROOT.gStyle.SetPalette(ROOT.kDarkBodyRadiator)
    ROOT.gStyle.SetPalette(ROOT.kBlueRedYellow)
    
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

    canname = 'RndSeq'
    can = ROOT.TCanvas(canname, canname, 0, 0, 1000, 1000)
    cans.append(can)
    
    N = 1024
    seq = MakeSequence(N)
    print(seq)
    marks = DrawSeq(can, seq)

    can.Print(can.GetName() + '.png')
    
    stuff.append(seq)
    stuff.append(marks)
    
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

