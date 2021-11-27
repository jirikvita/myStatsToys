#!/usr/bin/python

import ROOT
from math import sqrt
from math import fabs

data = [
    [2017,	49],
    [2016,	62],
    [2015,	60],
    [2014,	55],
    [2013,	50],
    [2012,	63],
    [2011,	59],
    [2010,	85],
    [2009,	97],
    [2008,	78],
    [2007,	97]
]

tag = ''
ShiftX = True
#ShiftX = False

UsePoissonErrors = True
#UsePoissonErrors = False

gr = ROOT.TGraphErrors()
i = 0
for point in data:
    xx = point[0]
    if ShiftX:
        xx = xx - 2000
    gr.SetPoint(i, xx, point[1])
    if UsePoissonErrors:
        gr.SetPointError(i, 0., sqrt(1.*point[1]))
    i = i+1
    
gr.SetMarkerSize(1)
gr.SetMarkerStyle(20)
gr.SetMarkerColor(ROOT.kBlack)

xmin = 2006
xmax = 2018

if ShiftX:
    tag = '_shifted'
    xmin = xmin - 2000
    xmax = xmax - 2000


tmp = ROOT.TH2D('tmp', 'tmp;rok-2000;zemreli na silnicich v rijnu', 100, xmin, xmax, 100, 0, 130)
tmp.SetStats(0)
ROOT.gStyle.SetOptTitle(0)

fitfun = ROOT.TF1('linfit', '[0]+[1]*x', xmin, xmax)
fitfunUp =   ROOT.TF1('linfitUp',   '[0]+[1]*x + sqrt( ([3]*x)^2 + [2]^2)', xmin, xmax)
fitfunDown = ROOT.TF1('linfitDown', '[0]+[1]*x - sqrt( ([3]*x)^2 + [2]^2)', xmin, xmax)
fitfun.SetParameters(1.,-1.)
if not ShiftX:
    fitfun.SetParameters(8000,-4.)

fitfun.SetNpx(200)
fitfun.SetLineColor(ROOT.kRed)
gr.Fit('linfit')
gr.Fit('linfit')
gr.Fit('linfit')
gr.Fit('linfit')
tmp.Draw()
gr.Draw('P')

chi2 = fitfun.GetChisquare()
ndf = fitfun.GetNDF()
if ndf > 0:
    print('chi2/ndf = %f / %i = %f' % (chi2, ndf, chi2/ndf, ))
    for ip in range(0, fitfun.GetNpar()):
        print('par%i=%f error=%f relerr=%f' % (ip, fitfun.GetParameter(ip), fitfun.GetParError(ip), fitfun.GetParError(ip) / abs(fitfun.GetParameter(ip)) ))

    print('Setting parameters for the fit error band!')
    fitfunDown.SetParameters( fitfun.GetParameter(0),  fitfun.GetParameter(1),  fitfun.GetParError(0),  fitfun.GetParError(1) )
    fitfunUp.SetParameters(   fitfun.GetParameter(0),  fitfun.GetParameter(1),  fitfun.GetParError(0),  fitfun.GetParError(1) )

    fitfun.DrawCopy('same')
    fitfunDown.SetLineColor(fitfun.GetLineColor())
    fitfunUp.SetLineColor(fitfun.GetLineColor())
    fitfunDown.SetLineStyle(2)
    fitfunUp.SetLineStyle(2)
    fitfunDown.DrawCopy('same')
    fitfunUp.DrawCopy('same')

    
    text1 = ROOT.TLatex(0.63, 0.83, '#chi^{2}/ndf' + ' = {:2.1f} / {:}'.format(fitfun.GetChisquare(), fitfun.GetNDF()))
    text1.SetNDC()
    text1.Draw()


ROOT.gPad.Print('LinFit' + tag + '.pdf')
ROOT.gPad.Print('LinFit' + tag + '.png')
ROOT.gApplication.Run()
