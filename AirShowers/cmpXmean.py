#!/usr/bin/python

# jk 6.9.2024
# jk 3.10.2025
# jk 6.12.2025

import ROOT
from math import pow, log10, pow, sqrt

import os, sys

from utils import *
from consts import *

########################################

cans = []
stuff = []

########################################
# to avoid Fit fluctuations / instabilities
# in Xmax and sigmaXmax:
kLowestXmaxToConsider = 10.
kHighestXmaxToConsider = 1200.
########################################

def AddToHeatMap(h2, h):
    for ibin in range(1, h.GetXaxis().GetNbins()+1):
        x = h.GetBinCenter(ibin)
        y = h.GetBinContent(ibin)
        h2.Fill(x,y)

########################################

def suspectedWideShower(realE, meanMean, h):
    #return (realE/1000 >= 100 and ( h.GetRMS() / meanMean > 0.55*( 300./realE + 1. ) ) ) or (realE/1000 < 100 and ( h.GetRMS() / meanMean > 0.70*( 300./realE + 1. ) ) ):
    if meanMean > 0:
        return  h.GetRMS() / meanMean > 0.80
    return False
        
########################################
# actually, getting maximum of shower development for each shower,
# i.e. really Xmax, by highest bin, so no mean X, 
# but then computing the mean of these Xmax values;)
def GetHmeans(logEs, fnames, hbasename, Nshowers, plotSigma, stdDevVsXmaxHists = None, debug = 0):
    Fs = []
    Hs = {}
    Means = {}
    Rebin = 1

    fit = ROOT.TF1('gfit', '[0]*exp(-0.5*(x-[1])^2/(2*[2]^2))', 0, 4000)
    for logE in logEs:
        infile = None
        #fname = fnames[logE]
        Hs[logE] = []
        means = []
        #print(f'Have {len(fnames[logE])} ROOT files')
        for fname in fnames[logE]:
            infile = ROOT.TFile(fname, 'read')
            Fs.append(infile)
            for i in range(0,Nshowers):
                hname = hbasename + f'_{i}'
                h = infile.Get(hname)
                try:
                    mean = None
                    err = None
                    imax = h.GetMaximumBin()
                    mean = h.GetBinCenter(imax)
                    A = h.GetBinContent(imax)
                    err = h.GetMeanError()
                    stdDev = h.GetStdDev()
                    fit.SetParameters(A, mean, 0.3*stdDev)
                    # fit around 5 bins around max
                    bw = h.GetBinWidth(imax)
                    h.Fit(fit, "Q", "", mean - 3*bw, mean + 3*bw)
                    mean = fit.GetParameter(1)
                    
                    if mean > kLowestXmaxToConsider and mean < kHighestXmaxToConsider:
                        means.append(mean)
                        if stdDevVsXmaxHists != None:
                            if logE in stdDevVsXmaxHists:
                                stdDevVsXmaxHists[logE].Fill(mean, stdDev)
                    
                        #print(mean)
                        if Rebin > 1:
                            h.Rebin(Rebin)
                        #flogE = float(logE)
                        #if flogE < 10e4:
                        #    h.Rebin(2)
                        Hs[logE].append(h)
                    else:
                        print(f'ERROR! Fitted Xmax {mean} out of range [{kLowestXmaxToConsider},{kHighestXmaxToConsider}]!')
                except:
                    if debug: 
                        print(f'Error getting {hname} from {fname}')
                    pass

        meanMean, meanErr = GetMeanAndError(means, plotSigma)
        Means[logE] = showerAverResults(logE, meanMean, meanErr, means)

    return Hs, Fs, Means
        
########################################
# TO CONSIDER: a check to get all this the Xmax'es from shower graphs -> histos maxima!

def GetHmeansFromTree(conexDir, EconexDict, treename, varname, plotSigma): #, stdDevVsXmaxHists_conex = None):
    Fs = []
    Hs = {}
    Means = {}
    for logE in EconexDict:
        Hs[logE] = []
        means = []
        
        fname = EconexDict[logE]
        rfile = ROOT.TFile(conexDir + fname, 'read')
        Fs.append(rfile)

        tree = rfile.Get(treename)
        hname = f'h_{logE}'
        h = ROOT.TH1D(hname, ';X_{max} [g/cm^{2}];showers', 150, 100, 1000)
        tree.Draw(f'{varname} >> {hname}', f'{varname} < 4000')
        # this is already a histogram of Xmax'es!
        #h = ROOT.gDirectory.Get(hname)
        #try:
        mean = None
        err = None
        # HERE take RMS to plot average Xmax sigma
        if plotSigma:
            mean = h.GetStdDev()
            err = h.GetStdDevError()
        else:
            # so we should NOT take maximum of the Xmax histo, but a mean!!!
            #mean = h.GetBinCenter(h.GetMaximumBin()) #h.GetMean()
            #err = h.GetMeanError()
            # so the mean:
            mean = h.GetMean()
            err = h.GetMeanError()

        means.append(mean)
        #print(mean)
        #h.Rebin(Rebin)
        #flogE = float(logE)
        #if flogE < 10e3:
        #    h.Rebin(2)
        Hs[logE].append(h)
        #meanMean, meanErr = GetMeanAndError(means)
        Means[logE] = showerAverResults(logE, mean, err, means)
        #except:
        #    print(f'Error getting conex {hname} from {fname}')


    return Hs, Fs, Means
        
        

########################################
def GetMeanAndError(means, plotSigma):
    meanSqSum = 0
    stdDev = 0.
    np = len(means)
    meanMean = sum(means) / np
    for i in range(0, len(means)):
        meanSqSum += pow(means[i] - meanMean, 2)
    meanErr = 0.
    if np > 1 and meanSqSum > 0:
        meanErr = sqrt(meanSqSum / (np - 1) / np)
        stdDev =  sqrt(meanSqSum / (np - 1))
    if not plotSigma:
        return meanMean, meanErr
    else:
        return stdDev, 0.

########################################
########################################
########################################

class showerAverResults:
    def __init__(self, logE, mean, meanErr, means):
        self.logE = logE
        self.mean = mean
        self.meanErr = meanErr
        self.means = means
  
########################################
########################################
########################################
      

def main(argv):

    SetMyStyle()
    sigmaTag = ''

    # DEFAULT:
    plotSigma = False
    #plotSigma = True
    
    ytitle = '<X_{max}>'
    if plotSigma:
        sigmaTag = '_sigma'
        ytitle = '#sigma_{X_{max}}'

    alllogEs = [#11, 11.5,
        ## Fe: remove 12 and 12.5
        '12',
        # useless: '12.25',
        '12.5',
        '12.75',
        '13',
        '13.25',
        '13.5',
        '14',
        '14.5',
        '14.75',
        '15',
        '15.25',
        '15.5',
        '15.75',
        '16',
    ]

    print(alllogEs)
    
    hbasename = 'h1Nx'
    Nshowers =  10001 # some supremum;)
    fnames = {}

    if len(argv) < 2:
        print(f'Usage:   {argv[0]} rootdir [model=EPOS,SIBYLL] [-b] (batch mode)')
        print(f'Example: {argv[0]} root_Inel_0.3_C_10.0_piExp_0.2 SIBYLL')
        return()
    
    onerootdir = argv[1]
    rootdirs = [onerootdir]

    # HACK:
    # sum two standardly generated showers!
    if 'testNoNewPhysWithNewPhysArea' in onerootdir:
        print('OK, adding one more standard directory to take graphs from!')
        rootdirs = ['root_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0', onerootdir]
    print('Will take ROOT files from:')
    print(rootdirs)
    
    generator = 'EPOS'
    if len(argv) > 2:
        generator = argv[2] # EPOS, SIBYLL

    gBatch = False
    if len(argv) > 3 and argv[3] == '-b':
        gBatch = True
        ROOT.gROOT.SetBatch(1)

    # primary particle as generated by AirSim:
    primary = 'p'
    #primary = 'A56'
    if 'primaryE' in rootdirs[0]:
        primary = 'e'
    if 'Fe' in rootdirs[0] or '56' in rootdirs[0]:
        primary = 'A56'
    print(f'Primary: {primary}')

    logEs = []
    for logE in alllogEs:
        flogE = float(logE)
        if flogE <= 12.75 and 'Zprime_100.0' in rootdirs[0] and 'mode_mumu' in rootdirs[0]:
            continue
        if flogE <= 14.75 and 'Zprime_1000.0' in rootdirs[0] and 'mode_mumu' in rootdirs[0]:
            continue
        if flogE > 14.6 and 'Zprime_100.0' in rootdirs[0]:
            continue
        
        for rootdir in rootdirs:
            fname = f'{rootdir}/histos_{primary}_logE_{flogE:1.1f}_tmp.root'
            if os.path.exists(fname):
                if not logE in fnames:
                    fnames[logE] = []        
                    logEs.append(logE)
                fnames[logE].append(fname)
    
    print(fnames)

    stdDevVsXmaxHists = {}
    if not plotSigma:
        for logE in logEs:
            stdDevVsXmaxHists[logE] = ROOT.TH2D(f'hist2D_StdDevVsXmax_{logE}', ';X_{max} [g/cm^{2}];X_{max} std. dev. [g/cm^{2}]', 100, 0, 1000, 100, 0, 500)

    Hs, Fs, MeansAirSim = GetHmeans(logEs, fnames, hbasename, Nshowers, plotSigma, stdDevVsXmaxHists)
        
    ftag = fnames[logEs[-1]][0].split('/')[-2].replace('root_','').replace('_',' ')
    fftag = ftag.replace(' ','_')
    if primary != 'p':
        ftag = ftag + ' ' + primary
        fftag = fftag + '_' + primary
    
    print('Got following lengths:')
    for logE in Hs:
        print(f'{logE}: {len(Hs[logE])}')
    
    gr = ROOT.TGraphErrors()
    gr.SetName('gr_airsim')
    ip = 0

    for logE,meanData in MeansAirSim.items():
        flogE = float(logE)
        mean = meanData.mean
        meanErr = meanData.meanErr
        gr.SetPoint(ip, flogE, mean)
        gr.SetPointError(ip, 0., meanErr)
        ip = ip+1

    conexDir='conex/simulated_showers/uniqueE_low/merged/'
    conexPrimary = 'p'
    if 'A56' in primary or 'Fe' in primary:
        conexPrimary = 'Fe'
    print(f'Conex primary: {conexPrimary}')
    EconexDict = {}
    conexlogEs = []
    for logE in logEs: #here
        fname = f'conex_{conexPrimary}_E_{logE}_{generator}_merged.root'
        if os.path.exists(conexDir + fname):
            EconexDict[logE] = fname
            conexlogEs.append(logE)

    cfnames = EconexDict.values()
    #stdDevVsXmaxHists_conex = {}
    #if not plotSigma:
    #    for logE in logEs:
    #        stdDevVsXmaxHists_conex[logE] = ROOT.TH2D(f'hist2D_StdDevVsXmax_conex_{logE}', ';X_{max} [g/cm^{2}];X_{max} std. dev. [g/cm^{2}]', 50, 0, 1000, 50, 0, 500)


    conexPeakXmaxHs, cFs, MeansConex = GetHmeansFromTree(conexDir, EconexDict, 'Shower', 'Xmax', plotSigma)# , stdDevVsXmaxHists_conex)
    
    gr_conex = ROOT.TGraphErrors()
    gr_conex.SetName('gr_conex')
    ip = 0
    ConexShowerGraphs = {}
    ConexShowerHistos = {}
    h2sXmaxCorrTest = {}
    crfiles = {}
    for logE,meanData in MeansConex.items():
        flogE = float(logE)
        mean = meanData.mean
        meanErr = meanData.meanErr
        gr_conex.SetPoint(ip, flogE, mean)
        gr_conex.SetPointError(ip, 0., meanErr)
        ip = ip+1

        # get also individual conex showers as TGraphs:
        rfile = ROOT.TFile(conexDir + EconexDict[logE], 'read')
        tree = rfile.Get('Shower')
        #graphs = getConexShowerGraphs(tree, logE)
        graphs, chistos, h2XmaxCorrTest = getAndCompareConexShowerGraphsMaxAndXmax(tree, logE)
        ConexShowerGraphs[logE] = graphs
        ConexShowerHistos[logE] = chistos
        #print('Printing histos for now....', logE, chistos)
        h2sXmaxCorrTest[logE] = h2XmaxCorrTest
        crfiles[logE] = rfile

    txts = []
    #print('ConexShowerHistos:')
    #print(ConexShowerHistos)


    # PLOTTING, CANVAS SPLITTING
    cnx, cny = 2, 2
    if len(ConexShowerGraphs) > 4:
        cnx, cny = 3, 3
    if len(ConexShowerGraphs) > 9:
        cnx, cny = 4, 3
    if len(ConexShowerGraphs) > 12:
        cnx, cny = 4, 4
    cw, ch = 1400, 1200

    ########################
    # Draw conex profiles as graphs
    canname = f'ConexGrProfiles'
    cpcan = ROOT.TCanvas(canname, canname, 0, 0, cw, ch)
    cans.append(cpcan)
    cpcan.Divide(cnx, cny)
    cpH2s = []
    ie = 0
    for logE,grs in ConexShowerGraphs.items():
        cpcan.cd(1+ie)
        ymax = getGrMaxima(grs)*1.2
        h2 = ROOT.TH2D(f'conexProfileGr_tmp_{logE}', ';x[g/cm^{2}];N', 100, 0, 4000, 100, 0, ymax)
        h2.Draw()
        makeWhiteAxes(h2)
        cpH2s.append(h2)
        opt = 'L'
        igr = 0
        for cgr in grs:
            if igr > 1000:
                break
            cgr.Draw(opt)
            igr += 1
            #opt = 'L'
        
        mtxt = ROOT.TLatex(0.59, 0.68, f'Conex+{generator}')
        mtxt.SetTextColor(ROOT.kWhite)
        mtxt.SetNDC()
        mtxt.Draw()
        txts.append(mtxt)

        ntxt = ROOT.TLatex(0.59, 0.75, f'Showers: {igr-1}')
        ntxt.SetTextColor(ROOT.kWhite)
        ntxt.SetNDC()
        ntxt.Draw()
        txts.append(ntxt)

        txt = ROOT.TLatex(0.59, 0.82, f'logE={logE}')
        txt.SetTextColor(ROOT.kWhite)
        txt.SetNDC()
        txt.Draw()
        txts.append(txt)
        
        ie += 1
    cpcan.Update()

    ########################
    # Draw conex profiles as histos:)
    stdDevVsXmaxHists_conex = {}
    canname = f'ConexHistProfiles'
    hcpcan = ROOT.TCanvas(canname, canname, 0, 0, cw, ch) 
    cans.append(hcpcan)
    hcpcan.Divide(cnx, cny)
    hcpH2s = []
    ie = 0
    nConexDoublePeaks = {}
    ConexHsDouble = {}
    for logE,grs in ConexShowerGraphs.items():
        if not plotSigma:
            stdDevVsXmaxHists_conex[logE] = ROOT.TH2D(f'hist2D_StdDevVsXmax_conex_{logE}', ';X_{max} [g/cm^{2}];X_{max} std. dev. [g/cm^{2}]', 100, 0, 1000, 100, 0, 500)

        nConexDoublePeaks[logE] = 0
        ConexHsDouble[logE] = []
        hcpcan.cd(1+ie)
        ymax = getGrMaxima(grs)*1.55
        h2 = ROOT.TH2D(f'conexProfileHist_tmp_{logE}', ';x[g/cm^{2}];N', 100, 0, 4000, 100, 0, ymax)
        h2.Draw()
        makeWhiteAxes(h2)
        hcpH2s.append(h2)
        #hs = makeHistosFromGraphs(grs, f'_{logE}')
        hs = ConexShowerHistos[logE]
        print(h2)
        # here can fill the Xmax std dev vs the Xmax!!
        if logE in stdDevVsXmaxHists_conex:
            #print(ConexShowerHistos[logE])
            for h in hs:
                stdDevVsXmaxHists_conex[logE].Fill(h.GetBinCenter(h.GetMaximumBin()), h.GetStdDev())
        
        ConexShowerHistos[logE] = hs
        opt = 'histsame'
        igr = 0
        meanMean = 0.
        for h in hs:
            val = h.GetMean()
            meanMean += val
        meanMean /= (1.*len(hs))

        for h in hs:
            if igr > 1000:
                break
            h.SetLineColor(ROOT.kCyan)
            flogE = float(logE)
            realE = pow(10, flogE)
            if suspectedWideShower(realE, meanMean, h):
                h.SetLineColor(ROOT.kRed)
                nConexDoublePeaks[logE] += 1
                ConexHsDouble[logE].append(h)

            h.Draw(opt)
            igr += 1
            #opt = 'L'

        stxt = ROOT.TLatex(0.63, 0.68, f'Conex+{generator}')
        stxt.SetTextColor(ROOT.kWhite)
        stxt.SetNDC()
        stxt.Draw()
        txts.append(stxt)

        ntxt = ROOT.TLatex(0.63, 0.75, f'Showers: {igr-1}')
        ntxt.SetTextColor(ROOT.kWhite)
        ntxt.SetNDC()
        ntxt.Draw()
        txts.append(ntxt)

        txt = ROOT.TLatex(0.63, 0.82, f'logE={logE}')
        txt.SetTextColor(ROOT.kWhite)
        txt.SetNDC()
        txt.Draw()
        txts.append(txt)
        
        ie += 1
        
    ie = 0
    for logE,hs in ConexHsDouble.items():
        hcpcan.cd(1+ie)
        for h in hs:
            h.Draw('same hist')
        ie += 1
    ie = 0
    for logE,hs in ConexShowerHistos.items():
        nConexDoublePeaks[logE] /= len(hs)
        print('Double peaks fraction: ', nConexDoublePeaks[logE])
        hcpcan.cd(1+ie)
        txt = ROOT.TLatex(0.15, 0.82, f'Double peaks frac.: {nConexDoublePeaks[logE]:1.3f}')
        txt.SetNDC()
        txt.SetTextColor(ROOT.kWhite)
        txt.Draw()
        stuff.append(txt)
        ie += 1


 
    
    
    ########################
    # Draw conex peak Xmax distributions (these are NOT shower profiles!:):
    canname = f'ConexPeakXmax'
    ccan = ROOT.TCanvas(canname, canname, 0, 0, cw, ch)
    cans.append(ccan)
    ccan.Divide(cnx, cny)
    cH2s = []
    ie = 0

    for logE,hs in conexPeakXmaxHs.items():
        ccan.cd(1+ie)
        ymax = getMaxima(hs)*1.55
        
        h2 = ROOT.TH2D(f'ctmp_{logE}', ';' + ytitle+ '[g/cm^{2}];showers', 150, 100, 900, 100, 0, 0.12)
        h2.Draw()
        makeWhiteAxes(h2)
        cH2s.append(h2)
        opt = ' same'
        for h in hs:
            h.SetLineWidth(1)
            h.SetStats(0)
            h.SetLineColor(ROOT.kRed)
            area = h.Integral()
            if area > 0:
                h.Scale(1./area)
            h.Draw('hist' + opt)
        ie += 1

    ccan.Update()
    
    H2s = []
    Hsums = []
    canname = f'CmpXmean'
    can = ROOT.TCanvas(canname, canname, 0, 0, cw, ch)
    cans.append(can)
    can.Divide(cnx, cny)

    canname = f'SumXmean'
    sumcan = ROOT.TCanvas(canname, canname, 600, 0, cw, ch)
    cans.append(sumcan)
    sumcan.Divide(cnx, cny)


    ########################
    # Plot private shower profiles
    ie = 0
    nDoublePeaks = {}
    HsDouble = {}
    # for histograms of peak Xmax vals, to be compared to already plotted conex;-)
    HsPeakXmax = {}
    for logE,hs in Hs.items():
        can.cd(1+ie)
        print(f'  logE={logE}, have histograms: {len(hs)}')
        HsDouble[logE] = []
        ymax = getMaxima(hs)*1.55
        h2 = ROOT.TH2D(f'tmp_{logE}', ';x[g/cm^{2}];Particles (e/#pi/p)', 100, 40, 4000, 100, 0, ymax)
        h2.Draw()
        makeWhiteAxes(h2)
        H2s.append(h2)

        HsPeakXmax[logE] = ROOT.TH1D(f'AirSimPeakXmax_{logE}', ';' + ytitle + '[g/cm^{2}];showers', 150, 100, 1000)

        h2sum = ROOT.TH2D(f'hsum_{logE}', ';x[g/cm^{2}];Particles (e/#mu)', 40, 0, 4000, 25, 0, ymax)
        makeWhiteAxes(h2sum)
        Hsums.append(h2sum)

        stxt = ROOT.TLatex(0.59, 0.68, 'Private sim.')
        stxt.SetTextColor(ROOT.kWhite)
        stxt.SetNDC()
        stxt.Draw()
        txts.append(stxt)

        txt = ROOT.TLatex(0.63, 0.82, f'logE={logE}')
        txt.SetTextColor(ROOT.kWhite)
        txt.SetNDC()
        txt.Draw()
        txts.append(txt)

        ntxt = ROOT.TLatex(0.59, 0.75, f'Showers: {len(hs)}')
        ntxt.SetTextColor(ROOT.kWhite)
        ntxt.SetNDC()
        ntxt.Draw()
        txts.append(ntxt)

        opt = ' same'
        meanMean = 0.
        # no filling by means of shower profiles,
        # but actually filling by already found Xmax vals!
        for val in MeansAirSim[logE].means:
            #for h in hs:
            #val = h.GetMean()
            meanMean += val
            HsPeakXmax[logE].Fill(val)
            #print('mean, rms: ', h.GetMean(), h.GetRMS())
        meanMean /= (1.*len(hs))
        #print('meanMean ', meanMean)
        nDoublePeaks[logE] = 0.
        for h in hs:
            h.SetLineWidth(1)
            h.SetStats(0)
            #print('...drawing, mean=', h.GetMean())
            #h.Draw('hist plc' + opt)
            h.SetLineColor(ROOT.kAzure-3)
            flogE = float(logE)
            realE = pow(10, flogE)
            if suspectedWideShower(realE, meanMean, h):
            
                h.SetLineColor(ROOT.kRed)
                nDoublePeaks[logE] += 1
                HsDouble[logE].append(h)
            h.Draw('hist' + opt)
            opt = ' same'
            AddToHeatMap(h2sum, h)
        #ROOT.gPad.BuildLegend()
        ROOT.gPad.RedrawAxis()
        #ROOT.gPad.SetGridx(1)
        #ROOT.gPad.SetGridy(1)
        ROOT.gPad.Update()

        sumcan.cd(1+ie)
        y1 = 1.5*h2sum.GetYaxis().GetBinWidth(1)
        h2sum.GetYaxis().SetRangeUser(y1, h2sum.GetYaxis().GetXmax())
        h2sum.Draw('colz')
        ROOT.gPad.Update()

        ie += 1
        #
    ie = 0
    for logE,hs in HsDouble.items():
        can.cd(1+ie)
        for h in hs:
            h.Draw('same hist')
        ie += 1
    ie = 0
    for logE,hs in Hs.items():
        nDoublePeaks[logE] /= len(hs)
        print('Double peaks fraction: ', nDoublePeaks[logE])
        can.cd(1+ie)
        txt = ROOT.TLatex(0.15, 0.82, f'Double peaks frac.: {nDoublePeaks[logE]:1.3f}')
        txt.SetNDC()
        txt.SetTextColor(ROOT.kWhite)
        txt.Draw()
        stuff.append(txt)
        ie += 1

    # plot histo of peak Xmax for AirSim into already plotted conex;-)
    ie = 0
    for logE,h in HsPeakXmax.items():
        ccan.cd(1+ie)
        area = h.Integral()
        if area > 0:
            h.Scale(1./area)
        h.SetLineWidth(1)
        h.SetStats(0)
        h.SetLineColor(ROOT.kAzure-3)
        h.Draw('hist same')
        txt = ROOT.TLatex(0.63, 0.82, f'logE={logE}')
        txt.SetTextColor(ROOT.kWhite)
        txt.SetTextSize(0.07)
        txt.SetNDC()
        txt.Draw()
        txts.append(txt)
        ie += 1
    ccan.Update()
    
    canname = 'GrXmean'
    gcan = ROOT.TCanvas(canname, canname, 500, 500, 800, 600)
    makeGrStyle(gr, ROOT.kAzure-3)
    gr.GetXaxis().SetTitle('log_{10}E(eV)')
    gr.GetYaxis().SetTitle(ytitle + ' [g/cm^{2}]')
    gr.GetYaxis().SetRangeUser(0, 1000)
    if plotSigma:
        gr.GetYaxis().SetRangeUser(0, 300)

    # private AirSim fit:
    gr.Draw('APL')
    fun = ROOT.TF1("fit", "[0] + [1]*x", 12., 20.)
    fun.SetParameters(500, 0.1)
    fun.SetLineStyle(7)
    fun.SetLineColor(gr.GetLineColor())
    fun.SetLineWidth(1)
    gr.Fit('fit')
    predict17 = fun.Eval(17.)
    print('Fit extrapolation to 10^17 eV: ', predict17)
    gr.GetYaxis().SetAxisColor(ROOT.kWhite)
    gr.GetYaxis().SetLabelColor(ROOT.kWhite)
    gr.GetYaxis().SetTitleColor(ROOT.kWhite)

    # conex fit
    makeGrStyle(gr_conex, ROOT.kRed)
    gr_conex.Draw('PL')
    cfun = ROOT.TF1("cfit", "[0] + [1]*x", 12., 20.)
    cfun.SetParameters(500, 0.1)
    cfun.SetLineStyle(7)
    cfun.SetLineColor(gr_conex.GetLineColor())
    cfun.SetLineWidth(1)
    gr_conex.Fit('cfit', '', '0')
    cfun.Draw('same')

    ROOT.gPad.SetGridx(1)
    ROOT.gPad.SetGridy(1)

    leg = ROOT.TLegend(0.15, 0.65, 0.66, 0.88)
    leg.AddEntry(gr, f'Private AirSim {ftag}', 'PL')
    leg.AddEntry(gr_conex, f'Conex + {generator}', 'PL')
    leg.SetTextColor(ROOT.kWhite)
    leg.Draw()

    chi2, ndf = getChi2(gr_conex, gr)
    chi2ndf = 0.
    if ndf > 0:
        chi2ndf = chi2/ndf
    chtxt = '#chi^{2}/ndf = ' + f'{chi2ndf:1.1f}'
    txt = ROOT.TLatex(0.62, 0.15, chtxt)
    txt.SetNDC()
    txt.SetTextColor(ROOT.kWhite)
    ###txt.Draw()
    
    ROOT.gPad.Update()

    stuff.append([leg, txt])

    ########################
    # print
    pngdir  = 'png_tuning/'
    pdfdir  = 'pdf_tuning/'

    cpcan.Update()
    cpcan.Print(pdfdir + cpcan.GetName() + f'_{generator}{sigmaTag}.pdf')
    cpcan.Print(pngdir + cpcan.GetName() + f'_{generator}{sigmaTag}.png')
    
    hcpcan.Print(pdfdir + hcpcan.GetName() + f'_{generator}{sigmaTag}.pdf')
    hcpcan.Print(pngdir + hcpcan.GetName() + f'_{generator}{sigmaTag}.png')
    
    can.Print(pngdir + can.GetName() + f'_{fftag}{sigmaTag}.png')
    can.Print(pdfdir + can.GetName() + f'_{fftag}{sigmaTag}.pdf')

    sumcan.Print(pngdir + sumcan.GetName() + f'_{fftag}{sigmaTag}.png')
    sumcan.Print(pdfdir + sumcan.GetName() + f'_{fftag}{sigmaTag}.pdf')
    
    gcan.Print(pngdir + gcan.GetName() + f'_{generator}_{fftag}{sigmaTag}.png')
    gcan.Print(pdfdir + gcan.GetName() + f'_{generator}_{fftag}{sigmaTag}.pdf')

    ccan.Print(pngdir + ccan.GetName() + f'_{generator}_{fftag}{sigmaTag}.png')
    ccan.Print(pdfdir + ccan.GetName() + f'_{generator}_{fftag}{sigmaTag}.pdf')

    stuff.append([conexPeakXmaxHs, Hs, H2s, cH2s, Fs, cFs, gr, gr_conex])

    print('Writing graphs to output file....')
    rootdir = 'graphs/'
    os.system(f'mkdir -p {rootdir}')
    outfilename = rootdir + f'graphs_{generator}_{fftag}{sigmaTag}.root'
    outfile = ROOT.TFile(outfilename, 'recreate')
    grs_to_save = [gr, gr_conex]
    for savegr in grs_to_save:
        savegr.Write()
        
    for logE,h2 in stdDevVsXmaxHists.items():
        h2.Write()
    for logE,h2 in stdDevVsXmaxHists_conex.items():
        h2.Write()
    for logE,h2 in h2sXmaxCorrTest.items():
        h2.Write()
        
    print('...closing output file...')
    outfile.Close()
    print('DONE!')
        
    
    if not gBatch:
        ROOT.gApplication.Run()
    os.system('killall -9 cmpXmean.py')


###########################################################
###########################################################
###########################################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)

###########################################################
###########################################################
###########################################################
