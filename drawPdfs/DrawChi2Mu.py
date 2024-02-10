#!/usr/bin/python

# jiri kvita, 4--11.11.2016



from myAll import *
#from PdfTools import *
from GraphicsTools import *

from ROOT import kGreen, kBlue, kRed

funs = []

def MakeAsymErrors(h1, delta = 1.):
    g1 = ROOT.TGraphAsymmErrors()
    g1.SetName('%s_gr' % (h1.GetName()))
    delta = math.fabs(delta)
    j=0
    for i in range(1,h1.GetNbinsX()+1):
        val = h1.GetBinContent(i)
        if val > 0:
            g1.SetPoint(j, h1.GetBinCenter(i), val)
            sigma1 = -0.5*delta + math.sqrt(val*delta + 0.25*delta*delta)
            g1.SetPointError(j, 0, 0, sigma1, sigma1+delta )
            j=j+1
    return g1

############################################

xmin = 0
xmax = 50.

# function of x=mu given k=observed data


pars = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
cols = [#kGreen,
        #kGreen+1,
        kGreen+2, kGreen+3,kGreen+4,
        kBlue, kBlue+1, kBlue+2, kBlue+3,
        kRed, kRed+1, kRed+2, kRed+3,
]


chi2s = []
canname = "Chi2Mu"
can = nextCan.nextTCanvas(canname, canname, 0, 0, 1600, 800)
can.Divide(2,1)


can.cd(1)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()

opt=''
for par in pars:
    j=pars.index(par)
    chi2 = ROOT.TF1('chi2_%i' % (j,), '(x-[0])^2/x', xmin, xmax) # axis titles: ;#mu;#chi^{2}(#mu,k)
    chi2.SetParameter(0,par)
    chi2.SetNpx(1000)
    chi2.SetLineColor(cols[j])
    chi2.Draw(opt)
    opt='same'
    chi2s.append(chi2)

can.cd(2)
ROOT.gPad.SetGridx() ; ROOT.gPad.SetGridy()
sf = 20.
sig1ratio = ROOT.TF1('ratio1', '(-1/2+sqrt(x+1/4.))/sqrt(x)', xmin, sf*xmax)
sig2ratio = ROOT.TF1('ratio2', '(1/2+sqrt(x+1/4.))/sqrt(x)', xmin, sf*xmax)
sig1ratio.SetLineStyle(1)
sig1ratio.SetNpx(1000)
sig2ratio.SetLineStyle(2)
sig2ratio.SetNpx(1000)
h2 = ROOT.TH2D('help', 'help;k;errors ratio to #sqrt{k}    ', 100, xmin, sf*xmax, 100, 0.85, 1.15)
h2.SetStats(0)
h2.Draw()
sig2ratio.Draw('same')
sig1ratio.Draw('same')

can.Print(canname + ".png")
can.Print(canname + ".pdf")
#can.Print(canname + ".eps")


canname = "AsymExample"
can2 = nextCan.nextTCanvas(canname, canname, 0, 0, 1000, 1000)
#can2.Divide(2,1)
grs = []
nbins = 20
x1 = -5
x2 = 5
h1 = ROOT.TH1D('test', 'test', nbins, x1, x2)
Nevt = 300

# https://root.cern.ch/doc/master/classTF1.html
# gaus(0) is a substitute for [0]*exp(-0.5*((x-[1])/[2])**2) 
fun = ROOT.TF1('fun1', '[0]*(1.+[1]*x+gaus(2))', x1, x2)
fun.SetParameters(1.*Nevt, -0.3, 5., 1.75, 1.)
funs.append(fun)

h1.FillRandom('fun1', Nevt)
h2 = ROOT.TH2D('t2', 't2', nbins, x1, x2, nbins, 0, 1.35*h1.GetMaximum())

g1 = MakeAsymErrors(h1, 1.)
can2.cd()
g1.SetMarkerColor(1)
g1.SetMarkerSize(1)
g1.SetMarkerStyle(20)

h2.SetStats(0)
h2.Draw()
print 'Fitting the original histogram:'
h1.Fit('fun1', '0')
text0 = ROOT.TLatex(0.170, 0.865, 'Histogram sym. errors fit: #chi^{2}/ndf' + ' = {:2.1f} / {:}'.format(fun.GetChisquare(), fun.GetNDF()))
text0.SetNDC()
text0.SetTextSize(0.03)
text0.Draw()

fun_hfit = fun.Clone('fun_hfit')
fun_hfit.SetLineStyle(2)
funs.append(fun_hfit)

g1.Draw('P')
grs.append(g1)
print 'Fitting the TGraphAsymmErrors:'
g1.Fit('fun_hfit', '')

fun.Draw('same')
fun_hfit.Draw('same')

text1 = ROOT.TLatex(0.170, 0.815, 'Graph asym. errors fit:    #chi^{2}/ndf' + ' = {:2.1f} / {:}'.format(fun_hfit.GetChisquare(), fun_hfit.GetNDF()))
text1.SetNDC()
text1.SetTextSize(0.03)
text1.Draw()


can2.Print(canname + ".png")
can2.Print(canname + ".pdf")


ROOT.gApplication.Run()
