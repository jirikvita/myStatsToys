#!/usr/bin/python

# JK Oct  7  2015
# modified 12.1.2018

from ROOT import *
from math import log

def fun_u_exp(x, tau, a, b):
    return -tau * log((b-x)/(b-a))

def fun_u_1over(x, a, b, u1, u2):
    return u1*pow(u2/u1, (x-a) / (b-a) )

def fun_u_negpower(x, a, b, alpha, u1):
    return u1 / pow( (b-x) / (b-a), 1/(alpha-1))

def MakeAxis(nbins, x1, x2):
    axis = TAxis(nbins, x1, x2)
    return axis


def DrawLines(U, u0, u1, u2, y1, y2, SF, showrate):
    iu = -1
    lines = []
    for uvec in U:
        iu = iu+1
        if iu % showrate == 0:
            ux = u0 + SF*(uvec - u1) / (u2 - u1)
            line = TLine(ux, y1, ux, y2)
            line.SetNDC()
            line.Draw()
            lines.append(line)
    return lines


rand = TRandom3()
# any a < b works;)
a=4
b=80
N=10000

hists = []
axes = []
u1 = []
u2 = []

axes.append(MakeAxis(100, a, b))


# exp. falling function
tau = 10.
u1_exp = 0.
# upper edge just for drawing purposes:
u2_exp = 100. # as this goes to infty: fun_u_exp(a,tau,a,b)
u1.append(u1_exp)
u2.append(u2_exp)
hist_exp = TH1D("gen_exp", "gen_exp;u;generated events", 100, u1_exp, u2_exp)
axis_exp = MakeAxis(100, u1_exp, u2_exp)
axes.append(axis_exp)

hists.append(hist_exp)

# 1/x falling function
# need a finite interval to make 1/u integrable
u1_1over = 1.
u2_1over = 101.
u1.append(u1_1over)
u2.append(u2_1over)
hist_1over = TH1D("gen_1over", "gen_1over;u;generated events", 100, u1_1over, u2_1over)
hists.append(hist_1over)
axis_1over = MakeAxis(100, u1_1over, u2_1over)
axes.append(axis_1over)

# negatively falling
# need a finite interval to make 1/u integrable

u1_negpower = 1.
# upper edge just for drawing purposes:
u2_negpower = 101.
u1.append(u1_negpower)
u2.append(u2_negpower)
alpha = 3.
hist_negpower = TH1D("gen_negpower", "gen_negpower;u;generated events", 100, u1_negpower, u2_negpower)
hists.append(hist_negpower)
axis_negpower = MakeAxis(100, u1_negpower, u2_negpower)
axes.append(axis_negpower)


can = TCanvas("GenDistr", "GenDistr", 0, 0, 1200, 800)
can.Divide(3,2)

xs = []
u_exp = []
u_1over = []
u_negpower = []

for i in range(0,N):
    x = rand.Uniform(a,b)
    xs.append(x)
    
    u = fun_u_exp(x, tau, a, b)
    #print x,u
    hist_exp.Fill(u)
    u_exp.append(u)
    
    u = fun_u_1over(x, a, b, u1_1over, u2_1over)
    hist_1over.Fill(u)
    u_1over.append(u)
    
    u = fun_u_negpower(x, a, b, alpha, u1_negpower)
    hist_negpower.Fill(u)
    u_negpower.append(u)
    
gStyle.SetOptTitle(0)
#hists = [hist_exp, hist_1over, hist_negpower]
for hist in hists:
    hist.SetStats(0)
    #hist.GetXaxis().SetLabelOffset(0.07)
    #hist.GetYaxis().SetLabelOffset(0.07)
    hist.GetXaxis().SetTitleOffset(1.04)
    hist.GetYaxis().SetTitleOffset(1.04)
    hist.GetXaxis().SetTitleSize(0.05)
    hist.GetYaxis().SetTitleSize(0.05)


can.cd(1)
hist_exp.SetMarkerColor(kBlack)
hist_exp.SetLineColor(kBlack)
hist_exp.SetMarkerSize(1)
hist_exp.SetMarkerStyle(22)
hist_exp.Draw('e1')
fun_exp = TF1('fun_exp', '[0]*exp(-[1]*x)', u1_exp, u2_exp)
fun_exp.SetParameters(1, 1)
hist_exp.Fit('fun_exp')
gPad.SetLogy(1)

can.cd(2)
hist_1over.SetMarkerColor(kBlack)
hist_1over.SetLineColor(kBlack)
hist_1over.SetMarkerSize(1)
hist_1over.SetMarkerStyle(22)
hist_1over.Draw('e1')
fun_1over = TF1('fun_1over', '[0] / x', u1_1over, u2_1over)
fun_1over.SetParameter(0, 1)
hist_1over.Fit('fun_1over')
hist_1over.GetXaxis().SetMoreLogLabels(1)
gPad.SetLogx(1)
gPad.SetLogy(1)

can.cd(3)
hist_negpower.SetMarkerColor(kBlack)
hist_negpower.SetLineColor(kBlack)
hist_negpower.SetMarkerSize(1)
hist_negpower.SetMarkerStyle(22)
hist_negpower.Draw('e1')
fun_negpower = TF1('fun_negpower', '[0] / x^[1]', u1_negpower, u2_negpower)
fun_negpower.SetParameters(1, 3.2345)
hist_negpower.Fit('fun_negpower')
hist_negpower.GetXaxis().SetMoreLogLabels(1)
gPad.SetLogx(1)
gPad.SetLogy(1)


Us = [u_exp, u_1over, u_negpower]

xlabel = TLatex(0.1, 0.75, "x")
xlabel.SetNDC(1)
ylabel = TLatex(0.1, 0.35, "u(x)")
ylabel.SetNDC(1)

i=1
Lines = []
showrate = 10
u0 = 0.1
SF = 0.8
y1 = 0.2
y2 = 0.3
iU = -1
for U in Us:
    iU = iU+1
    can.cd(4+iU)
    lines = DrawLines(U, u0, u1[iU], u2[iU], y1, y2, SF, showrate)
    Lines.append(lines)
    ylabel.Draw()
    xlabel.Draw()

showrate = 100
iU = -1
for U in Us:
    iU = iU+1
    can.cd(4+iU)
    xlines = DrawLines(xs, u0, a, b, y1+0.4, y2+0.4, SF, showrate)
    Lines.append(xlines)
    showrate = showrate + 1
        
gApplication.Run()
