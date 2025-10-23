#!/usr/bin/python3

from utils import *

from numpy.random import exponential as exponential
from numpy.random import poisson as Poisson

from math import sqrt, pow, log, exp, log10
import os, sys, getopt
import random


Nevts = 50000

# radiation length
length = 37.
maxNlengthsEM = 10

hx = ROOT.TH1D('customDecaySamplingX', ';x;N;', 200, 0, 10*length)
hf = ROOT.TH1D('customDecaySamplingFracE', ';frac;N;', 200, 0, 1.)
hfinclcompl = ROOT.TH1D('customDecaySamplingFracEinclComplementary', ';frac;N;', 200, 0, 1.)

for i in range(0, Nevts):
    dx = 10*maxNlengthsEM*length
    while dx > maxNlengthsEM*length:
        dx = exponential(length)
    xi = exp(-dx / length)
    # in simulation we then move the particle by dx
    # x = min(part.x + dx, world.x2)
    hx.Fill(dx)
    hf.Fill(xi)
    hfinclcompl.Fill(xi)
    hfinclcompl.Fill(1. - xi)

cn = 'testExpDecayMeans'
can = ROOT.TCanvas(cn, cn, 0, 0, 1200, 600)
can.Divide(2,1)

can.cd(1)
#hx.Scale(1./hx.Integral())
hx.SetFillStyle(1111)
hx.SetFillColor(ROOT.kYellow)
hx.Draw('hist')
ROOT.gPad.SetLogy(1)

can.cd(2)
hf.SetFillStyle(1111)
hf.SetFillColor(ROOT.kGreen)
hf.SetMinimum(0.)
hf.Draw()

#can.cd(3)
#hfinclcompl.SetFillStyle(1111)
#hfinclcompl.SetFillColor(ROOT.kCyan)
#hfinclcompl.SetMinimum(0.)
#hfinclcompl.Draw()


can.Update()
ROOT.gApplication.Run()
