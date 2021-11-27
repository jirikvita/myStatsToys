#!/usr/bin/python
# Mon 26 Aug 10:10:43 CEST 2019
# jk

from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

cans = []
stuff = []

##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):


    ROOT.gRandom = ROOT.TRandom3(314);


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

    canname = 'can1'
    can1 = ROOT.TCanvas(canname, canname, 0, 0, 600, 600)
    canname = 'can2'
    can2 = ROOT.TCanvas(canname, canname, 650, 0, 600, 600)
    #can.Divide(2,1)
    cans.append(can1)
    cans.append(can2)
    #filename = 'foo.root'
    #rfile = ROOT.TFile(filename, 'read')

    x1 = -6.
    x2 = -x1
    
    myfun = ROOT.TF1('myfun', '[0] + [1]/(1 + [2]*x^2) +  [3]* ( 1./(1 + [4]*(x-[5]-[6])^2) +  1./(1 + [4]*(x-[5]+[6])^2) ) ', x1, x2)
    cc = 42538000
    # singlet:
    c1 = -60000.
    # some inverse width parameter
    inw1 = 5
    # doublet:
    c2 = 0.35 * c1
    inw2 = 5.
    shift = 0.75
    delta = 0.75
    myfun.SetParameters(cc, c1, inw1, c2, inw2, shift, delta)

    can1.cd()
    myfun.Draw()

    hname = 'histo'
    iRep = 20 # 20
    # test: nbins = int(15*(x2-x1))
    # nbins = int((x2-x1))
    ###default
    nbins = int(43*(x2-x1))
    
    print('Nbins: {}'.format(nbins))
    h1 = ROOT.TH1D(hname, hname, nbins, x1, x2)
    stuff.append(h1)
    Nrq = int(cc*nbins/iRep)
    # percentae of additionally generated events
    ptcl = 6 # 6
    additional = int(ptcl/100.*Nrq)
    print('Generating {} events...'.format(iRep*Nrq))
    for i in range(0, iRep):
        print('Round {}/{}...'.format(i+1, iRep))
        h1.FillRandom('myfun', Nrq+additional)
    can2.cd()
    h1.SetMarkerStyle(20)
    h1.SetMarkerSize(0.7)
    h1.Draw('P')

    can1.Update()
    can2.Update()

    tag = ''
    if ptcl > 0:
        tag = '_add{}ptcl'.format(ptcl)
    can2.Print(can2.GetName() + tag + '.C')
    can2.Print(can2.GetName() + tag + '.png')
    can2.Print(can2.GetName() + tag + '.pdf')
    
    print('DONE!')

    
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

