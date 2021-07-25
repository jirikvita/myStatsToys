#!/usr/bin/python

import ROOT
import os, sys

filename = 'banka.txt'
infile = open(filename, 'r')

col = [ROOT.kBlack, ROOT.kBlue, ROOT.kGreen+2, ROOT.kRed,
       ROOT.kBlack, ROOT.kBlue, ROOT.kGreen+2, ROOT.kRed,
       ROOT.kBlack, ROOT.kBlue, ROOT.kGreen+2, ROOT.kRed]
tags = []
hists = []
phists = []
h2 = []

nBins=10
x1 = -0.5
x2 = 9.5

for i in range(0,4):
    if i < 3:
        tags.append('Group%i' % (i+1,))
    else:
        tags.append('AllGroups')
    hists.append(ROOT.TH1D(tags[-1], tags[-1], nBins, x1, x2))

ptags = []
h2names = []

Npos = 2*4+3

for i in range(0,Npos):
    ptags.append('Position%i' % (i+1,))
    phists.append(ROOT.TH1D(ptags[-1], ptags[-1], nBins, x1, x2))
for i in range(0,Npos):
    for j in range(i,Npos):
        hname = 'scatter_%i_%i' % (i,j,)
        h2names.append(hname)
        h2.append(ROOT.TH2D(hname, hname,  nBins, x1, x2,  nBins, x1, x2))
    
nl=-1
for xline in infile.readlines():
    nl=nl+1
    line = xline[0:-1]
    #print line
    triplets = line.split()
    it = -1
    ip = -1
    for tri in triplets:
        it = it+1
        for cif in tri:
            ip = ip+1
            hists[it].Fill(int(cif))
            hists[-1].Fill(int(cif))
            phists[ip].Fill(int(cif))
    lline = line.replace(' ', '')
    for i in range(0, len(lline)):
        for j in range(i, len(lline)):
            hname = 'scatter_%i_%i' % (i,j,)
            k = h2names.index(hname)
            h2[k].Fill(int(lline[i]), int(lline[j]))

print 'OK, read %i lines!' % (nl,)


canname = 'GroupHistos'      
can = ROOT.TCanvas(canname, canname, 0, 0, 1000, 1000)
can.Divide(2,2)
for hist in hists:
    j = hists.index(hist)
    can.cd(j+1)
    hist.SetMinimum(0.)
    hist.SetLineColor(col[j])
    hist.SetMarkerColor(col[j])
    hist.SetMarkerStyle(20+j)
    hist.SetMarkerSize(1)
    hist.Draw("e1hist")


name = 'chi2OverNdf'
nCif = len(phists)
chi2h = ROOT.TH1D(name, name+';position;#chi^{2}/ndf', nCif, 0, nCif)

NDF = nBins-1 # 10 digits, one constant fit parameter
chi2hist = ROOT.TH1D(name, name+';#chi^{2}', 5, 0, 2*(NDF+1))

pcanname = 'PositionHistos'      
pcan = ROOT.TCanvas(pcanname, pcanname, 0, 0, 1000, 1000)
pcan.Divide(4,3)
fun = ROOT.TF1('myfun', '[0]', -1, 10)
for phist in phists:
    j = phists.index(phist)
    pcan.cd(j+1)
    phist.SetMinimum(0.)
    phist.SetLineColor(col[j])
    phist.SetMarkerColor(col[j])
    phist.SetMarkerStyle(20+j)
    phist.SetMarkerSize(1)
    phist.Draw("e1hist")
    fun.SetParameter(0, phist.Integral() / (1.*phist.GetNbinsX()) )
    print'Fitpar set to %f' % (fun.GetParameter(0), )
    phist.Fit('myfun', '0q')
    fun.DrawCopy('same')
    ndf = fun.GetNDF()
    chi2 = fun.GetChisquare()
    if ndf > 0:
        print 'Chi2/ndf = %f / %i, p0=%f' % ( chi2, ndf, fun.GetParameter(0))
        chi2ndf = chi2 / ndf
        chi2h.Fill(j, chi2ndf)
        chi2hist.Fill(chi2)




chicanname = 'Chi2'
chican = ROOT.TCanvas(chicanname, chicanname, 50, 50, 1600, 800)
chican.Divide(2,1)
chican.cd(1)
chi2h.SetMarkerStyle(20)
chi2h.SetMarkerSize(1)
chi2h.SetMarkerColor(ROOT.kBlack)
chi2h.SetStats(0)
chi2h.Draw('p')
ROOT.gPad.SetGridx(1)
ROOT.gPad.SetGridy(1)
chican.cd(2)
chi2hist.SetMarkerStyle(21)
chi2hist.SetMarkerSize(1)
chi2hist.SetMarkerColor(ROOT.kBlack)
chi2hist.Draw('e1')
funchi = ROOT.TF1('chi2fit', '[0]*x^[1]*exp(-x/2)', 0., chi2hist.GetXaxis().GetXmax())
# http://mathworld.wolfram.com/Chi-SquaredDistribution.html
funchi.SetParameters(1., NDF/2.-1.)
chi2hist.Fit('chi2fit', '0')
funchi.Draw('same')
ndf = funchi.GetNDF()
chi2 = funchi.GetChisquare()
print 'Fit of the chi2 shape: chi2/ndf = %f / %i' % ( chi2, ndf,)


canname2 = 'ScatterHistos'      
can2 = ROOT.TCanvas(canname2, canname2, 200, 200, 1000, 1000)
can2.Divide(11,11,0.,0.)
#k=-1
#for h in h2:
#    k = k+1
#    can2.cd(k+1)
#    h.Draw('colz')
for i in range(0,Npos):
    for j in range(i,Npos):
        hname = 'scatter_%i_%i' % (i,j,)
        k = h2names.index(hname)
        can2.cd(i*Npos+j+1)
        marg = 0.
        ROOT.gPad.SetTopMargin(marg)
        ROOT.gPad.SetBottomMargin(marg)
        ROOT.gPad.SetLeftMargin(marg)
        ROOT.gPad.SetRightMargin(marg)
    

        h2[k].SetStats(0)
        h2[k].Draw('colz')


hcorr = ROOT.TH2D('Corrs', 'Corrs', Npos, 0, Npos, Npos, 0, Npos)
hcorr_nodiag = ROOT.TH2D('CorrsNoDiag', 'CorrsNoDiag', Npos, 0, Npos, Npos, 0, Npos)
for i in range(0,Npos):
    for j in range(i,Npos):
        hname = 'scatter_%i_%i' % (i,j,)
        k = h2names.index(hname)
        corr = h2[k].GetCorrelationFactor()
        hcorr.Fill(i, j, corr)
        if i != j:
            hcorr_nodiag.Fill(i, j, corr)

cannamecorr = 'CorrHisto'      
cancorr = ROOT.TCanvas(cannamecorr, cannamecorr, 0, 0, 1600, 800)
cancorr.Divide(2,1)
cancorr.cd(1)
#hcorr.SetMinimum(-1.)
#hcorr.SetMaximum(1.)
hcorr.SetStats(0)
hcorr.Draw('colz')
cancorr.cd(2)
hcorr_nodiag.SetStats(0)
hcorr_nodiag.Draw('colz')


can.Print(can.GetName() + '.png')
can.Print(can.GetName() + '.pdf')
pcan.Print(pcan.GetName() + '.png')
pcan.Print(pcan.GetName() + '.pdf')
chican.Print(chican.GetName() + '.png')
chican.Print(chican.GetName() + '.pdf')
can2.Print(can2.GetName() + '.png')
can2.Print(can2.GetName() + '.pdf')
cancorr.Print(cancorr.GetName() + '.png')
cancorr.Print(cancorr.GetName() + '.pdf')


ROOT.gApplication.Run()
