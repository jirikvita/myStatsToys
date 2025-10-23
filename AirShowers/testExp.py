#!/usr/bin/python3

import ROOT
from math import sqrt, pow

stuff = []

N = 10
x0 = 5000
lmb = x0 * (N -1 ) / (N*(N-2))

form = '1/(  2*[1]^3*(1 - exp(-[0]/[1])) - [1]^2*[0]*(1 + exp(-[0]/[1])) ) * x * (x - [0]) * exp(-x/[1])'

fun = ROOT.TF1('fun', form, 0, x0)
fun.SetParameters(x0, lmb)

ROOT.gStyle.SetOptTitle(0)

fun.SetNpx(1000)
fun.Draw()
fun.GetXaxis().SetTitle('E [GeV]')
fun.GetYaxis().SetTitle('prob. density')

xmax = lmb + x0/2 - sqrt( pow(lmb,2) + pow(x0/2., 2) )
y1 = 0.
y2 = fun.Eval(xmax)
line = ROOT.TLine(xmax, y1, xmax, y2)
line.SetLineWidth(2)
line.SetLineStyle(2)
line.Draw()
print(f'xmax = {xmax}')

I = fun.Integral(0, x0)
print(f'Integral: {I:1.4f}')

ROOT.gPad.Update()

stuff.append([line, fun])

ROOT.gApplication.Run()
