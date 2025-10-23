#!/usr/bin/python3

from utils import *

E = 5000
N = 10
x0 = E
lmb = E / N
ymax =  ymax_pdf(x0, lmb)

Nevts = 10000
xs = [ sample_from_custom_pdf(x0, lmb, ymax) for i in range(0,Nevts) ]

print(x0, lmb)
print(ymax)
print(xs)

h = ROOT.TH1D('customSampling', '', 200, 0, E)
for x in xs:
    h.Fill(x)

h.SetFillStyle(1111)
h.SetFillColor(ROOT.kCyan)
h.Draw()


ROOT.gPad.Update()
ROOT.gApplication.Run()
