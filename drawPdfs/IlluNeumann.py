#!/usr/bin/python

# jiri kvita, 9.10.2015

from myAll import *
from ROOT import *

canname = 'vonNeumannIlu'
can = nextCan.nextTCanvas(canname, canname, 0, 0, 800, 800)
#can.Divide(2,1)


x1 = 0
x2 = 10
fun1 = TF1("fun1", "gaus(0)+gaus(3)+gaus(6)", x1, x2) 
pars = [2., 3, 0.5, 
        0.1, 5., 4, 
        0.45, 7, 1]
for i in range(0,len(pars)):
    print 'par%i=%f' % (i,pars[i])
    fun1.SetParameter(i, pars[i])
fun1.SetLineColor(kBlack)
ymax = fun1.GetMaximum()

#can.cd(1)
fun1.Draw()
lineMax = TLine(x1, ymax, x2, ymax)
lineMax.SetLineStyle(2)
lineMax.SetLineColor(kBlack)
lineMax.Draw()

x = 6.5
y = ymax/3.

lineX = TLine(x, 0, x, ymax)
lineX.SetLineStyle(2)
lineX.SetLineColor(kBlack)
lineX.Draw()

mark1 = TMarker(x,0, 20)
#mark1.SetMarkerStyle(21)
mark1.SetMarkerSize(1)
mark1.SetMarkerColor(kBlack)
mark1.Draw()

mark2 = TMarker(x,y, 20)
#mark2.SetMarkerStyle(21)
mark2.SetMarkerSize(1)
mark2.SetMarkerColor(kBlack)
mark2.Draw()

#can.Print('vonNeumannIlu.eps')
can.Print('vonNeumannIlu.png')
can.Print('vonNeumannIlu.pdf')

# ROOT.gPad.SetGridx() ; ROOT.gPad.SetGridy()

ROOT.gApplication.Run()
