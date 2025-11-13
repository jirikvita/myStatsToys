#!/usr/bin/python3

import ROOT

#brehm = ROOT.TF1('brehm', '1/(1-x) * (1 - 2./3.*x + x^2)', 0, 1)
#brehm = ROOT.TF1('brehm', '(1 - 2./3.*x + x^2)', 0, 1)
# x as the photon energy fraction
#brehm = ROOT.TF1('brehm', '(4./3. - 4./3.*x + x^2)', 0, 1)
# x as the electron energy fraction:
brehm = ROOT.TF1('brehm', '(4./3. - 4./3.*(1-x) + (1-x)^2)', 0, 1)


pair = ROOT.TF1('pair', '(1 - 4./3.*x*(1. - x) ) * 9./7.', 0, 1)
pair.SetLineColor(ROOT.kBlue)
pair.SetLineStyle(2)


h = ROOT.TH2D('hh',';x;;', 100, 0, 1, 100, 0, 4)
h.SetStats(0)
h.Draw()

pair.Draw('same')
brehm.Draw('same')

#ROOT.gPad.BuildLegend()
leg = ROOT.TLegend(0.15, 0.5, 0.9, 0.9)
leg.AddEntry(brehm, 'norm. Brehmstrahlung, x=surv. electron energy fraction', 'L')
leg.AddEntry(pair, 'norm. Pair production, x=electron energy fraction', 'L')
leg.Draw()

ROOT.gPad.Update()

print(f'brehm: I={brehm.Integral(0,1)}')
print(f'pair: I={pair.Integral(0,1)}')

ROOT.gApplication.Run()
