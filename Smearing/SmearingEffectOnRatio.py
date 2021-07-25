#!/usr/bin/python

import ROOT
from nextCan import *
from myPyStyle import *
from myHistoTools import *

# generate a pair of particles with the same pT, oposite in phi
# smear each pT independently by the same resolution function
# compute the ratio of the smeared pTs, two entries/event

x1=10.
x2=110.
nbins=100

can=next()
can.Divide(2,3)

# resolution:
genSpect = nextTF1("genSpect", "[0]*x*exp(-[1]*x)", x1, x2)
genSpect.SetParameters(1, 0.1)
can.cd(1)
genSpect.Draw()

genResCal = nextTF1("genResCal", "sqrt([0]*[0] + [1]*[1]/x^2)", 0., x2)
genResCal.SetParameters(4, 0.03)

genResTrk = nextTF1("genResTrk", "[0] + [1]*x", 0., x2)
genResTrk.SetParameters(0., 0.15)

# genRes=genResTrk
genRes=genResCal
can.cd(2)
genRes.Draw()

# pT spectrum generating histogram
genHist = nextH1("genHist", "genHist", int(1000), x1, x2)
genHist.FillRandom("genSpect",1000000)

Scatter = nextH2("scatter", "scatter;p_{T}^{(1)};p_{T}^{(2)}", nbins, x1, x2, nbins, x1, x2)

Ratio = nextH1("Ratio", "Ratio", int(200), 0., 4.)
Diff = nextH1("Diff", "Diff", int(400), x2/1.5, x2/1.5)

rand = ROOT.TRandom3()
events = 10000

for i in range(0,events):
    if (i % 1000) == 0:
        print "Processing %i" % (i,)
    pt1 = genHist.GetRandom()
    pt2 = pt1

    pt1 = pt1 + rand.Gaus(0, genRes.Eval(pt1))
    pt2 = pt2 + rand.Gaus(0, genRes.Eval(pt2))

    Scatter.Fill(pt1, pt2)
    Ratio.Fill(pt1/pt2)
    Ratio.Fill(pt2/pt1)
    Diff.Fill(pt1 - pt2)
    Diff.Fill(pt2 - pt1)

can.cd(3)
Scatter.Draw("colz")

can.cd(4)
ROOT.gPad.SetLogy()
ROOT.gPad.SetGridx()
Diff.Draw("colz")

can.cd(5)
# ROOT.gPad.SetLogy()
ROOT.gPad.SetGridx()
Ratio.Draw("colz")

can.cd(6)
ROOT.gPad.SetLogy()
ROOT.gPad.SetGridx()
Ratio.Draw("colz")


ROOT.gApplication.Run()
