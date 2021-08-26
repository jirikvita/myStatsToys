#!/usr/bin/python
# Wed 25 Aug 15:01:14 CEST 2021

from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

cans = []
stuff = []
hs = []

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

    rnd = ROOT.TRandom3()
    
    cans.append(can)
    # number of counts of some counting experiment
    count = 250
    # number of events for each random variable
    Nx = 500
    # number of random variables:
    Ns = [2, 10, 100, 1000]
    for N in Ns:
        hname = 'aver{}'.format(N)
        nbins = 100
        x1 = 0.85 * count*N
        x2 = 1.15*count*N
        h1 = ROOT.TH1D(hname, hname, nbins, x1, x2)
        hs.append(h1)
        Ys = []
        for ivar in range(0, N):
            ys = []
            for i in range(0, Nx):
                ys.append(rnd.Poisson(count))
            Ys.append(ys)
        for i in range(0, len(Ys[0])):
            aver = 0
            for iy in range(0, len(Ys)):
                aver = aver + Ys[iy][i]
            #aver = aver / N
            h1.Fill(aver)
    can.Divide(2,2)
    for h1 in hs:
        can.cd(hs.index(h1)+1)
        h1.Draw('hist')
        
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

