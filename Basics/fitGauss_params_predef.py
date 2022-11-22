#!/usr/bin/python

import os, sys

from math import pow, sqrt, pi
#from math import pow as Pow

#from math import sin, cos as cos,sin

import ROOT

stuff = []

###############################################

def fitGauss(Ngen = 1000):

    fname = 'myfun'
    formula = '[0]*exp(-(x-[1])^2 / (2*[2]^2))'
    x1, x2 = -5, 5
    fun = ROOT.TF1(fname, formula, x1, x2)
    fun.SetParameters(1., 0., 2.)

    hname = 'myhist_{}'.format(Ngen)
    title = 'gauss rnd;x[aux];y[arb];'
    nbins = 32
    h1 = ROOT.TH1D(hname, title, nbins, x1, x2)
    
    h1.FillRandom(fname, Ngen)

    cw = 1000
    ch = 800
    canname = 'gfit_{}'.format(Ngen)
    can = ROOT.TCanvas(canname, canname, 0, 0, cw, ch)
    can.cd()
    h1.SetMarkerStyle(20)
    h1.SetMarkerSize(2)
    h1.SetMarkerColor(ROOT.kBlack)

    ROOT.gStyle.SetOptFit(111)

    h1.Draw('e1')

    #h1.Fit(fname, '0q')
    h1.Fit(fname)
    fun.SetLineStyle(1)
    #fun.Draw('same')

    stuff.append([fun, h1, can])

    can.Update()
    can.Print(can.GetName() + '_{}.png'.format(Ngen))
    can.Print(can.GetName() + '_{}.pdf'.format(Ngen))
    


    return 0

###############################################

def main(argv):
   
    # Ngens = [10, 100, 1000]
    Ngens = [ int(pow(10,i)) for i in range(0, 5)]
    print(Ngens)
    
    
    for Ngen in Ngens:
        print('Generating {} events; Pi = {:1.5}'.format(Ngen, pi))
        fitGauss(Ngen)

    ROOT.gApplication.Run()


###############################################
###############################################
###############################################



if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)


    
