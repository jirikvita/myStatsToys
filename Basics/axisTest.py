#!/usr/bin/python

import ROOT

from array import array
vals = array('d', [0.,10., 20., 50., 100., 200., 1000.])
n = len(vals)
name = 'histo'
title = name + ';x [GeV];y [1/GeV];'
h = ROOT.TH1D(name, title, n-1, vals)
fun = ROOT.TF1('fun', '[0]*exp(-[1]*x)', vals[0], vals[-1])
tau = 0.01
fun.SetParameters(1./tau, tau)

N=10000
h.FillRandom('fun', N)
h.Draw()

ROOT.gApplication.Run()
