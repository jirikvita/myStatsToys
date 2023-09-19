#!/snap/bin/pyroot
# was: #!/usr/bin/python3
# jk 19.9.2023

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt
from random import gauss

cans = []
stuff = []


class var:
    def __init__(self, name, x1, x2, val, sigmas):
        self.name = name
        self.x1 = x1
        self.x2 = x2
        self.val = val
        self.sigmas = sigmas
        if len(sigmas) > 3:
            self.stat = sigmas[0]
            self.systCorr = sigmas[1]
            self.systUncorr = sigmas[2]
            self.lumi = sigmas[3]
    
def MakeHists(vars, nb = 100):
    hists = {}
    for var in vars:
        name = var.name
        title = var.name
        hists[name] = ROOT.TH1D(name, title, nb, var.x1, var.x2)
    return hists

def adjustStats(h):
    ROOT.gPad.Update()
    st = h.GetListOfFunctions().FindObject("stats")
    st = ROOT.gPad.GetPrimitive("stats")
    st.SetX1NDC(0.7)
    st.SetX2NDC(0.9)
    st.SetY1NDC(0.65)
    st.SetY2NDC(0.9)
    return

##########################################
def MakeRatioToys(w1, Ntoys = 100000):
   
    # https://indico.cern.ch/event/1325591/contributions/5577718/attachments/2716915/4719187/HITop-2023-09-19.pdf
    # ATLAS p+Pb 8.16 TeV
    # σtt = 57.9 ± 2.0 (stat.) +4.9 −4.5 (syst.) nb = 57.9 +5.3 −4.9 (tot.) nb
    # ATLAS pp 8 TeV arXiv:1406.5375 
    # σtt = 242.9 ± 1.7 (stat.) ± 5.5 (exp.+theo.) ± 5.1 (lumi.) pb = 242.9 ± 7.7 (tot.) pb
    # extrapolated: 242.9/1000 nb ∗ 208 ∗ (236.497 pb)/(224.56 pb)

    
  

    pb = 1.e-3
    nb = 1.
        
    # weights to split corr and uncorr systs
    # their sum in quadrature should be 1.
    w2 = sqrt(1. - pow(w1,2))
    
    # pPb
    x1, x2 = 30.*nb, 80.*nb # nb
    stat = 2.*nb
    # some split for the moment;)
    systCorr = nb*4.5 * w1
    systUncorr = nb*4.5 * w2
    lumi = 1.5*nb
    x0 = 57.9*nb
    X = var('pPb', x1, x2, x0, [stat, systCorr, systUncorr, lumi])
    
    # the pp value:
    ppstat = 1.7*pb 
    # some split for the moment;)
    ppsystCorr = pb*5.5 * w1
    ppsystUncorr = pb*5.5 * w2
    pplumi = pb*5.1
    y0 = 242.2*pb
    y1,y2 = 200.*pb, 300.*pb
    Y = var('pp', y1, y2, y0, [ppstat, ppsystCorr, ppsystUncorr, pplumi])       

    A = 208
    ExtrapolationC = A*236.497/224.56
    Z = var('ratio', 0.5, 1.5, x0/(y0*ExtrapolationC), [])
    
    #create histos for x, y and z
    Vars = [X, Y, Z]
    Hists = MakeHists(Vars)
    
    # loop
    for i in range(0,Ntoys):
        # throw randomly the syst and stat shifts in (un)correlated way
        # fill histograms
        randSystCorr = gauss(0.,1.)
        randXstat = gauss(0.,1.)
        randYstat = gauss(0.,1.)
        randXsyst = gauss(0.,1.)
        randYsyst = gauss(0.,1.)
        randXlumi = gauss(0.,1.)
        randYlumi = gauss(0.,1.)

        x = X.val + randSystCorr*X.systCorr + randXsyst*X.systUncorr + randXstat*X.stat + randXlumi*X.lumi
        y = Y.val + randSystCorr*Y.systCorr + randYsyst*Y.systUncorr + randYstat*Y.stat + randYlumi*Y.lumi
    
        z = x / (y*ExtrapolationC)
    
        Hists[X.name].Fill(x)
        Hists[Y.name].Fill(y)
        Hists[Z.name].Fill(z)
    
    # draw histograms
    canname = 'RatioToys'
    can = ROOT.TCanvas(canname, canname, 0, 0, 1500, 500)
    can.Divide(3,1)
    cans.append(can)
    ican = 1
    opt = 'hist'
    for name,hist in Hists.items():
        can.cd(ican)
        hist.SetLineColor(ROOT.kBlack)
        hist.SetLineWidth(1)
        hist.SetLineStyle(1)
        hist.SetMarkerColor(ROOT.kBlack)
        #hist.SetMarkerColor(20)
        hist.SetMaximum(1.2*hist.GetMaximum())
        hist.Draw(opt)
        adjustStats(hist)
        can.Update()
        ican = ican + 1 
    stuff.append(Hists)
    txt1 = ROOT.TLatex(0.13, 0.85, 'Corr. w={:1.2f} Uncorr w={:1.2f}'.format(w1,w2))
    txt1.SetTextSize(0.04)
    txt1.SetNDC()
    
    width = Hists[Z.name].GetStdDev()
    # analytical error propagation:
    print('*** For the analytical part:')
    print(X.val, X.systCorr,  X.systUncorr, X.stat, X.lumi)
    print(Y.val, Y.systCorr,  Y.systUncorr, Y.stat, Y.lumi)
    rho = 1.
    sigmaZsq = -2.*rho*X.systCorr*Y.systCorr/X.val/Y.val
    print(sigmaZsq)
    sigmaZsq = sigmaZsq + pow(X.systUncorr/X.val,2) + pow(X.stat/X.val,2) + pow(X.lumi/X.val,2) 
    print(sigmaZsq)
    sigmaZsq = sigmaZsq + pow(Y.systUncorr/Y.val,2) + pow(Y.stat/Y.val,2) + pow(Y.lumi/Y.val,2) 
    print(sigmaZsq)
    print(width, sigmaZsq)
    sigmaZ = 0.
    if sigmaZsq > 0:
        sigmaZ = Z.val*sqrt(sigmaZsq)
        
    txt2 = ROOT.TLatex(0.13, 0.78, 'Width={:1.3f}'.format(width))
    txt2.SetTextSize(0.04)
    txt2.SetNDC()
    stuff.append([txt1, txt2])
    txt1.Draw()
    txt2.Draw()
    can.Update()
    tag = '_w1_{:1.1f}_w2_{:1.1f}'.format(w1,w2).replace('.','p')
    can.Print(can.GetName() + tag + '.png')
    can.Print(can.GetName() + tag + '.pdf')
    werr = Hists[Z.name].GetStdDevError()
    return can, Hists, width, werr, sigmaZ

###################################
###################################
###################################


##########################################
def main(argv):
    n = 11
    gr = ROOT.TGraphErrors()
    grAnalytic = ROOT.TGraph()
    Hists = []
    Cans = []
    N = 10000
    for j in range(0,n):
        w1 = j/(1.*n-1)
        can, hists, width, werr, sigmaZ = MakeRatioToys(w1, N)
        gr.SetPoint(j, w1, width)
        gr.SetPointError(j, 0., werr)
        grAnalytic.SetPoint(j, w1, sigmaZ)   
        Hists.append(Hists)
        Cans.append(can)
    
    canname = 'RatioErrorEvolution'
    can = ROOT.TCanvas(canname, canname, 100, 100, 1000, 800)
    
    can.cd()
    gr.SetMarkerStyle(20)
    gr.SetMarkerSize(1)
    gr.SetMarkerColor(ROOT.kBlue)
    
    grAnalytic.SetMarkerStyle(20)
    grAnalytic.SetMarkerSize(1)
    grAnalytic.SetMarkerColor(ROOT.kBlack)
    
    gr.Draw('AP')
    gr.GetXaxis().SetTitle('w_{corr}')
    grAnalytic.Draw('P')
    
    can.Update()
    
    ROOT.gApplication.Run()
if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################

