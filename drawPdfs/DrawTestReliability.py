#!/usr/bin/python

# jiri kvita, 30.9.2014, 14.10.2015



from myAll import *
from PdfTools import *
from GraphicsTools import *


############################################

xmin = 0
xmax = 1

# reliaility = P(N) * P(+|N) / (P(N) * P(+|N) + (1-P(N)) * P(+|Z))
# P(N) ... fraction of sick people
# P(+|N) test efficiency on sick
# P(+|Z)) test inefficiency on healthy

funEff = ROOT.TF1('funEff', '1/(1 + (1-[0])*[1]/([0]*x))', xmin, xmax)
# paramas: P(N), ineff
funEff.SetParameters(0.25, 0.015)

funIneff = ROOT.TF1('funIneff', '1/(1 + (1-[0])*x/([0]*[1]))', xmin, xmax)
# paramas: P(N), eff
funIneff.SetParameters(0.25, 0.99)

funFrac = ROOT.TF1('funFrac', '1/(1 + (1-x)*[1]/(x*[0]))', xmin, xmax)
# paramas: eff, ineff
funFrac.SetParameters(0.99, 0.015)


canname = "TestReliability"
can = nextCan.nextTCanvas(canname, canname, 0, 0, 800, 800)
can.Divide(2,2)


can.cd(1)
ROOT.gPad.SetGridx() ; ROOT.gPad.SetGridy()
funEff.Draw()

can.cd(2)
ROOT.gPad.SetGridx() ; ROOT.gPad.SetGridy()
funIneff.Draw()

can.cd(3)
ROOT.gPad.SetGridx() ; ROOT.gPad.SetGridy()
funFrac.Draw()


can.Print(canname + ".png")
#can.Print(canname + ".eps")
can.Print(canname + ".pdf")

ROOT.gApplication.Run()
