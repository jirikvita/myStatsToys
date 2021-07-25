#!/usr/bin/python

# jk 1.11.2018

from ROOT import *

xmin = -5.
xmax = 5.

x = RooRealVar('x', 'x', xmin, xmax)

Mean = RooRealVar('Mean', 'Mean', 0., -30, 30)
Sigma = RooRealVar('Sigma', 'Sigma', 1., 0, 10)
gauss = RooGaussian('Gauss', 'Gauss', x, Mean, Sigma)

frame = x.frame()

can = TCanvas()
can.Divide(2,2)

can.cd(1)
gauss.plotOn(frame)
frame.Draw()

can.cd(2)
cgauss = gauss.createCdf(RooArgSet(x))
cgauss.plotOn(frame)
frame.Draw()

can.cd()
gPad.Print('pdfs.png')

# voight = RooVoigt('','', )
