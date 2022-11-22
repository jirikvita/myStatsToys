#!/usr/bin/python

import os, sys, math

import ROOT

stuff = []

###############################################

def fitGauss(Ngen = 1000):

    fname = 'myfun'
    formula = '[0]*exp(-(x-[1])^2 / (2*[2]^2))'
    x1, x2 = -5, 5
    fun = ROOT.TF1(fname, formula, x1, x2)
    fun.SetParameters(1., 0., 2.)

    hname = 'myhist'
    title = 'gauss rnd;x[aux];y[arb];'
    nbins = 32
    h1 = ROOT.TH1D(hname, title, nbins, x1, x2)
    
    h1.FillRandom(fname, Ngen)

    cw = 1000
    ch = 800
    canname = 'gfit'
    can = ROOT.TCanvas(canname, canname, 0, 0, cw, ch)
    can.cd()
    h1.SetMarkerStyle(20)
    h1.SetMarkerSize(2)
    h1.SetMarkerColor(ROOT.kBlack)

    ROOT.gStyle.SetOptFit(111)

    h1.Draw('e1')

    h1.Fit(fname)
    fun.SetLineStyle(1)
    fun.Draw('same')

    stuff.append([fun, h1, can])

    can.Update()
    can.Print(can.GetName() + '.png')
    can.Print(can.GetName() + '.pdf')

    ROOT.gApplication.Run()

    return 0

###############################################

def main(argv):
    if len(argv) < 2:
        print('Usage: {} Ngen'.format(argv[0]))
        return 1

    Ngen = 1000
    try:
        Ngen = int(argv[1])
    except ValueError:
        print("Couldn't convert argument 1 to int! Using default Ngen={}".format(Ngen))

    
    return fitGauss(Ngen)


###############################################
###############################################
###############################################



if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)


    
