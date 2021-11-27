#!/usr/bin/python

import os, sys, ROOT, math

def GetNumTag(i, digits=4):
    tag = str(i)
    n=digits
    try: 
        n = int(math.log10(i))
    except ValueError:
        pass
    if i is 0:
        n = 0
    for i in range(0, digits-n):
        tag = '0' + tag
    return tag

formula = "[0]*exp(-[1]*x) + [2]*exp(-(x-[3])^2 / (2*[4]^2))"
x1 = 10.
x2 = 150.
nbins = 35

fname = "generatingFunction"
fun = ROOT.TF1(fname, formula, x1, x2)
fitfun=fun.Clone('fitfun')
gamma=5.
purity=0.1
alfa=0.01
mass=110.
fun.SetParameters((1.-purity), alfa, 1.*purity, mass, gamma)
parnames = [ 'N_{BG}', 'slope', 'N_{sig}', 'Mass', 'width']
for i in range(0, len(parnames)):
    fun.SetParName(i, parnames[i])

# Ngen = [1000000, 50000, 10000, 5000, 1000]

#Col = [2, 4, 8, 4, 1]
#Mark = [20, 21, 22, 23, 24]
#hlist = []
Ngen = [ 200 ]
multi=1.1
for j in range(0,50):
    Ngen.append(int(multi*Ngen[-1]))


sameopt = ''
canname = 'can'
can = ROOT.TCanvas(canname, canname)

#for mark,col,ngen in zip(Mark,Col,Ngen):
j=-1

col = 1
mark = 20

hname = 'histo'
hist = ROOT.TH1D(hname, hname, nbins, x1, x2)
hist.Sumw2()
hist.SetMarkerStyle(mark)
hist.SetMarkerColor(col)
ROOT.gStyle.SetOptFit(111)

for ngen in Ngen:
    j=j+1
    tag = GetNumTag(j)
    print('=== Processing %i' % (ngen,)) 
    hname = 'histo_%i' % (ngen,)
    tmphist = ROOT.TH1D(hname, hname, nbins, x1, x2)
    tmphist.Sumw2()
    tmphist.FillRandom(fname, ngen)
    hist.Add(tmphist)
    #hist.Scale(1./hist.Integral())
    integral = hist.Integral()
    testmass = [x1 + i*(x2-x1)/nbins for i in range(1,nbins-1)]
    fitfun.SetParLimits(0, 0, integral)
    fitfun.SetParLimits(1, 0, 4*alfa)
    fitfun.SetParLimits(2, 0, integral)
    fitfun.SetParLimits(3, x1, x2)
    fitfun.SetParLimits(4, gamma/3., 3*gamma)
    for i in range(0, len(parnames)):
        fitfun.SetParName(i, parnames[i])
    bestchi2 = 1.e9
    bestmass = -1
    # testgamma = gamma
    testgamma = 1.
    for m in testmass:
        print('Testing mass  %f' % (m,))
        fitfun.SetParameters(0.8*integral, alfa, 0.2*integral, m, testgamma)
        hist.Fit(fitfun, 'Q')
        hist.Fit(fitfun, 'Q')
        chi2 = fitfun.GetChisquare()
        print('  m=%f, chi2=%f' % (m, chi2, ))
        if chi2 < bestchi2:
            bestchi2 = chi2
            bestmass = m
    print('  *** bestchi2=%f' % (bestchi2,))
    fitfun.SetParameters(0.8*integral, alfa, 0.2*integral, bestmass, testgamma)
    hist.Fit(fitfun, 'Q')
    hist.Fit(fitfun)      
    hist.Draw("e1" + sameopt)
    # hlist.append(hist)
    # sameopt = 'same'
    print(tag)
    can.Print("gif/%s_%s.gif" % (canname,tag))

anim='anim.gif'
os.system('cd gif/ ; rm %s; convert *.gif %s' % (anim, anim,))
ROOT.gApplication.Run()
