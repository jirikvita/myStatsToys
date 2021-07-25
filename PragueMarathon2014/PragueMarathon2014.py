#!/usr/bin/python

import ROOT, sys, os, math

import nextCan
import myPyStyle
import myHistoTools


ROOT.gStyle.SetOptStat(0)


# data cetnosti casu Prague International Marathon 2014, v binech 5 min.
Data = [0, 3, 4, 4, 7, 3, 
        5, 11, 14, 24, 51, 85,
        58, 81, 132, 166, 199, 258,
        257, 270, 312, 301, 336, 459,
        247, 261, 273, 242, 225, 222,
        190, 179, 160, 143, 124, 125,
        92, 61, 61, 77, 48, 53,
        44, 27, 23, 27, 22, 16,
        8, 19, 14, 2, 5, 0,
        4, 1, 2, 2, 0]

sum = 0
for i in Data:
    sum = sum + i
print 'Sum of all runners: %i' %(sum,)

t0 = 2*60+5
t1 = 6*60+50
delta = 5


Times = [t0 + x*delta for x in range(0, (t1 - t0)/delta + 1) ]

histo0 = nextCan.nextH1("raw", "raw;x;y", len(Data), 0, len(Data))
histo1 = nextCan.nextH1("data", "data;x;y", (t1-t0)/delta, t0, t1)
histo2 = nextCan.nextH1("dataErr", "data;x;y", (t1-t0)/delta, t0, t1)
histo3 = nextCan.nextH1("PragueMarathon2014", "PragueMarathon2014;minutes;runners", (t1-t0)/delta, t0, t1)

histo2.SetMarkerSize(1)
histo2.SetMarkerStyle(20)
histo3.SetMarkerSize(1)
histo3.SetMarkerStyle(20)

can = nextCan.nextTCanvas("Run", "Run", 0, 0, 1900, 1200)
can.Divide(3,2)

j = 0
for time,data in zip(Times,Data):
    histo0.SetBinContent(j, data)
    histo1.SetBinContent(j, data)
    histo2.SetBinContent(j, data)
    histo3.SetBinContent(j, data)
    histo2.SetBinError(j, math.sqrt(data))
    histo3.SetBinError(j, math.sqrt(data))
    j=j+1

can.cd(1)
histo0.Draw("hist")

can.cd(2)
histo1.Draw("hist")

can.cd(3)
histo2.Draw("e1")

can.cd(4)
histo3.DrawCopy("e1")


can.cd(5)
histo3.DrawCopy("e1")
# draw lines at 3h and 4h arrival times:
Data.sort()
line3 = ROOT.TLine(3*60, 0, 3*60, 1.1*Data[-1])
line3.SetLineColor(2)
line3.Draw()

line4 = ROOT.TLine(4*60, 0, 4*60, 1.1*Data[-1])
line4.SetLineColor(2)
line4.Draw()

line5 = ROOT.TLine(5*60, 0, 5*60, 1.1*Data[-1])
line5.SetLineColor(2)
line5.Draw()

can.Update()

can.Print("RunSummary.png")
can.Print("RunSummary.pdf")

can.cd(1)
ROOT.gPad.Print("RunCan1.png")

can.cd(2)
ROOT.gPad.Print("RunCan2.png")
can.cd(3)
ROOT.gPad.Print("RunCan3.png")
can.cd(4)
ROOT.gPad.Print("RunCan4.png")

can.cd(4)
ROOT.gPad.SetLogy(1)
ROOT.gPad.Print("RunCan4_log.png")

can.cd(5)
ROOT.gPad.Print("RunCan5.png")

ROOT.gApplication.Run()
