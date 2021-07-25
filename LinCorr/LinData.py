#!/usr/bin/python

import ROOT

ROOT.gStyle.SetOptTitle(0)

xmin = 40
xmax = 170.
mux = 110.
muy = 110.
sx = 15.
sy = 15.
rho = 0.65

# define a high intelligency:
high = 130

xx = ROOT.Double(0.)
yy = ROOT.Double(0.)

objs = []

# https://en.wikipedia.org/wiki/Multivariate_normal_distribution
form = '[0]*exp( -1/(2*(1-[5]^2)) * (  (x-[1])^2 / [2]^2 + (y-[3])^2/[4]^2 - 2*[5]*(x-[1])*(y-[3]) / ([2]*[4]) )  )'
name='IQ_2D'
gen = ROOT.TF2(name, form, xmin, xmax, xmin, xmax)
gen.SetParameters(1., mux, sx, muy, sy, rho)
npx = 500
#npx = 100
gen.SetNpx(npx)
gen.SetNpy(npx)
gen.GetXaxis().SetTitle('men IQ')
gen.GetYaxis().SetTitle('women IQ')

objs.append(gen)

canname = 'LinData'
can = ROOT.TCanvas(canname, canname, 0, 0, 1600, 800)
objs.append(can)
can.Divide(2,1)
can.cd(1)
gen.Draw("col")


N = 1000
gr = ROOT.TGraph()
gr.SetMarkerSize(0.7)
gr.SetMarkerStyle(20)
gr.SetMarkerColor(ROOT.kBlack)
objs.append(gr)

for i in range(0,N):
    gen.GetRandom2(xx, yy)
    #print 'x=%f, y=%f' % (xx,yy)
    gr.SetPoint(i,xx,yy)

# theoretical fun:
# https://stats.stackexchange.com/questions/32464/how-does-the-correlation-coefficient-differ-from-regression-slope
# https://www.thoughtco.com/slope-of-regression-line-3126232
# https://en.wikipedia.org/wiki/Multivariate_normal_distribution
# https://en.wikipedia.org/wiki/Best_linear_unbiased_prediction
fun = ROOT.TF1('lin', '[0]+[1]*x', xmin, xmax)
fun.SetParameters(-rho*sy/sx*mux+muy, rho*sy/sx)
fun.SetNpx(npx)
fun.SetLineColor(ROOT.kRed)
objs.append(fun)

# fit
fitfun = ROOT.TF1('linfit', '[0]+[1]*x', xmin, xmax)
fitfunUp =   ROOT.TF1('linfitUp',   '[0]+[1]*x + sqrt( ([3]*x)^2 + [2]^2)', xmin, xmax)
fitfunDown = ROOT.TF1('linfitDown', '[0]+[1]*x - sqrt( ([3]*x)^2 + [2]^2)', xmin, xmax)
fitfun.SetParameters(0.,1.)
fitfun.SetNpx(npx)
fitfun.SetLineColor(ROOT.kBlue)
objs.append(fitfun)
objs.append(fitfunUp)
objs.append(fitfunDown)


gr.Fit('linfit')
chi2 = fitfun.GetChisquare()
ndf = fitfun.GetNDF()
if ndf > 0:
    print 'chi2/ndf = %f / %i = %f' % (chi2, ndf, chi2/ndf, )
    for ip in range(0, fitfun.GetNpar()):
        print 'par%i=%f error=%f' % (ip, fitfun.GetParameter(ip), fitfun.GetParError(ip),)

    print 'Setting parameters for the fit error band!'
    fitfunDown.SetParameters( fitfun.GetParameter(0),  fitfun.GetParameter(1),  fitfun.GetParError(0),  fitfun.GetParError(1) )
    fitfunUp.SetParameters(   fitfun.GetParameter(0),  fitfun.GetParameter(1),  fitfun.GetParError(0),  fitfun.GetParError(1) )
    
help = ROOT.TH2D('tmp', 'tmp', 100, xmin, xmax, 100, xmin, xmax)
help.SetStats(0)
help.GetXaxis().SetTitle('men IQ')
help.GetYaxis().SetTitle('women IQ')

can.cd(2)
help.Draw()
gr.Draw('P')
fun.DrawCopy('same')
if ndf > 0:
    fitfunDown.SetLineColor(fitfun.GetLineColor())
    fitfunUp.SetLineColor(fitfun.GetLineColor())
    fitfunDown.SetLineStyle(2)
    fun.DrawCopy('same')
    fitfunUp.SetLineStyle(2)
    fitfunDown.DrawCopy('same')
    fitfunUp.DrawCopy('same')

line1 = ROOT.TLine(high, xmin, high, xmax)
line2 = ROOT.TLine(xmin, high, xmax, high)
line3 = ROOT.TLine(xmin, xmin, xmax, xmax)
line3.SetLineStyle(2)
line1.Draw()
line2.Draw()
line3.Draw()

can.cd(1)
line3.Draw()
fun.Draw('same')

can.Print(can.GetName() + '.pdf')
can.Print(can.GetName() + '.png')

ROOT.gApplication.Run()
