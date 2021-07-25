#!/usr/bin/python
# Thu  8 Jul 13:20:59 CEST 2021

# implement
# Kernel Estimation in High-Energy Physics
# Kyle S. Cranmer
# https://arxiv.org/abs/hep-ex/0011057

from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp, pi
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

    ROOT.gStyle.SetOptTitle(0)
    
    canname = 'can'
    can = ROOT.TCanvas(canname, canname)
    cans.append(can)
    #filename = 'foo.root'
    #rfile = ROOT.TFile(filename, 'read')

    x1 = 0
    x2 = 7
    gf = '[0]*exp(-(x-[1])^2 / (2*[2]^2) )'
    # events to fill the histogram
    N = 35
    
    orig = ROOT.TF1('orig', gf, x1, x2)
    # extra factor of 2 as we the fill in histo only the posive part of x axis;-)
    orig.SetParameters(2*N / (sqrt(2*pi)), 0., 1.)
    npx = 400
    orig.SetNpx(npx)
    print(orig.Integral(x1,x2))
    
    hname = 'histo_h'
    nb = 10
    h1 = ROOT.TH1D(hname, hname + ';x', nb, x1, x2)
    h1.SetStats(0)
    h1.SetLineWidth(2)
    h1.SetMarkerStyle(20)
    h1.SetLineColor(ROOT.kBlue)
    h1.SetMarkerColor(ROOT.kBlue)

   
    h1.FillRandom('orig', N)
    print(h1.Integral())
        
    h1.SetMaximum(2.*h1.GetMaximum())
    h1.Draw('e1')
    orig.Draw('same')
    kernels = []
    hpar = (x2 - x1) / (1.*nb)
    fnames = []
    for i in range(0, nb):
        fname = 'kernel_{}'.format(i)
        bcontent = h1.GetBinContent(i+1)
        bcenter = h1.GetBinCenter(i+1)
        #print(bcontent, bcenter)
        if bcontent < 1e-5:
            continue
        kernel = ROOT.TF1(fname, gf, x1, x2)
        kernel.SetNpx(npx)
        fnames.append(fname)
        A = bcontent / (1.*hpar) / (sqrt(2*pi))
        kernel.SetParameters(A, bcenter, hpar)
        kernel.SetLineStyle(2)
        kernel.SetLineWidth(2)
        kernel.SetLineColor(ROOT.kBlue)
        kernel.SetLineWidth(1)
        kernel.Draw('same') # plc
        kernels.append(kernel)

    totalfname = ''
    ip = 0
    for fname in fnames:
        sign = ' + '
        if totalfname == '':
            sign = ''
        totalfname = totalfname + sign + '[{}]*exp(-(x-[{}])^2 / (2*[{}]^2) )'.format(ip, ip+1, ip+2)
        ip = ip + 3
    print(totalfname)
    ftotname = 'totalPdf'
    totalPdf = ROOT.TF1(ftotname, totalfname, x1, x2)
    totalPdf.SetNpx(npx)
    totalPdf.SetLineStyle(2)
    ip = 0
    for kernel in kernels:
        np = kernel.GetNpar()
        for iip in range(0, np):
            totalPdf.SetParameter(ip+iip, kernel.GetParameter(iip))
        ip = ip + np
    totalPdf.Draw('same')

    h2 = h1.Clone('smoothed_generated')
    h2.Reset()
    # poissonize N?
    h2.FillRandom(ftotname, N)
    h2.SetMarkerStyle(25)
    h2.SetLineWidth(1)
    h2.SetLineColor(ROOT.kBlack)
    h2.SetMarkerColor(ROOT.kBlack)
    h2.Draw('e1 same')

    leg = ROOT.TLegend(0.55, 0.45, 0.88, 0.88)
    leg.SetBorderSize(0)
    leg.AddEntry(orig, 'Original PDF', 'L')
    leg.AddEntry(h1, 'Original rnd histo', 'P')
    leg.AddEntry(kernels[0], 'Kernels', 'L')
    leg.AddEntry(totalPdf, 'Kernel PDF', 'L')
    leg.AddEntry(h2, 'Rnd histo from Kernel', 'P')
    leg.Draw()
    
    can.Print('kernel.png')
    can.Print('kernel.pdf')
    
    stuff.append([h1, h2, totalPdf, orig, leg])
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

