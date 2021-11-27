#!/usr/bin/python

# jk 5.5.2016

from ROOT import *
from math import *

rand = TRandom3(0)

ls = [2, 2, 2, 1, 1]
lw = [1, 1, 2, 2, 2]
lc = [kRed, kRed+1, kRed+2, kBlue, kBlue+1]

def GetRatioOverToys(mu = 500, nToy = 1000, nExp = 100):
    name = 'sigmaRatios_%i_%i_%i' % (mu,nToy,nExp)
    title = '#mu = %i, toys: %i' % (mu, nToy,)
    h_sigmaRatios = TH1D(name, title+";#sigma/#sigma'", 110, 0, 3.)

    for ntoy in range(0,nToy):
        N = []
        for n in range(0,nExp):
            Ni = rand.Poisson(mu)
            N.append(Ni)
        averN = 0
        for Ni in N:
            averN = averN + Ni
        averN = averN / len(N)
        sigmaSq = 0
        for Ni in N:
            sigmaSq = sigmaSq + pow(averN - Ni, 2)
        sigmaSq = sigmaSq / (len(N)-1)
        sigma = sqrt(sigmaSq)
        sigmaAver = sigma / sqrt(len(N))
        sigmaAlt = sqrt(averN) / sqrt(len(N))
        ratio = sigmaAver / sigmaAlt
        # print ratio
        h_sigmaRatios.Fill(ratio)
    return h_sigmaRatios

Mu = 500
nToy = 1000
histos = []
nExps = [500, 100, 50, 10, 5]

#gStyle.SetOptTitle(0)

leg = TLegend(0.45, 0.5, 0.89, 0.87)

for nExp in nExps:
   print('Running nexp=%i' % (nExp,))
   histo = GetRatioOverToys(Mu, nToy, nExp)
   histo.SetStats(0)
   histos.append(histo)
   leg.AddEntry(histo, 'n_{exp}=%i mean=%1.2f RMS=%1.2f' % (nExp,histo.GetMean(), histo.GetRMS()), 'L')

same=''
i=0
for histo in histos:
    histo.SetLineWidth(lw[len(lw)-i-1])
    histo.SetLineStyle(ls[len(ls)-i-1])
    histo.SetLineColor(lc[i])
    histo.Draw('hist'+same)
    same = 'same'
    i=i+1

leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.Draw()
histos.append(leg)

gPad.Print('PoissonMeanTest_lin.png')
#gPad.Print('PoissonMeanTest_lin.eps')
gPad.Print('PoissonMeanTest_lin.pdf')
gPad.SetLogy(1)
gPad.Print('PoissonMeanTest_log.png')
#gPad.Print('PoissonMeanTest_log.eps')
gPad.Print('PoissonMeanTest_log.pdf')


gApplication.Run()

    
