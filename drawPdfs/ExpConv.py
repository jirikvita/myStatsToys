#!/usr/bin/python

# jiri kvita, 27.1.2017



from myAll import *
#from PdfTools import *
from GraphicsTools import *

from ROOT import kGreen, kBlue, kRed

############################################

xmin = 0
xmax = 50.
tau=2000.
tauScinti=2.

fun1 = ROOT.TF1('Exp', '[0]*exp(-[0]*x)', xmin, xmax)
fun1.SetParameter(0, 1./tau)
fun1.SetLineStyle(2)
fun1.SetLineColor(ROOT.kBlack)


fun2 = ROOT.TF1('ExpExp', '[0]*[1]/([1]-[0])*(exp(-[0]*x) - exp(-[1]*x))', xmin, xmax)
fun2.SetParameters(1./tau, 1./tauScinti)
fun2.SetLineStyle(1)
fun2.SetLineColor(ROOT.kRed)

canname = 'ExpExp'
can = nextCan.nextTCanvas(canname, canname, 0, 0, 1600, 800)
#can.Divide(2,1)
#can.cd(1)
ROOT.gPad.SetGridx() ; ROOT.gPad.SetGridy()

fun1.Draw()
fun2.Draw('same')




can.Print(canname + ".png")
#can.Print(canname + ".eps")
can.Print(canname + ".pdf")
