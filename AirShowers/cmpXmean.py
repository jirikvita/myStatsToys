#!/usr/bin/python

#jk 6.9.2024
import ROOT
from math import pow, log10, pow, sqrt

import os, sys

from utils import *
from consts import *

########################################

cans = []
stuff = []

########################################

def AddToHeatMap(h2, h):
    for ibin in range(1, h.GetXaxis().GetNbins()+1):
        x = h.GetBinCenter(ibin)
        y = h.GetBinContent(ibin)
        h2.Fill(x,y)

########################################

def suspectedWideShower(realE, meanMean, h):
    #return (realE/1000 >= 100 and ( h.GetRMS() / meanMean > 0.55*( 300./realE + 1. ) ) ) or (realE/1000 < 100 and ( h.GetRMS() / meanMean > 0.70*( 300./realE + 1. ) ) ):
    return  h.GetRMS() / meanMean > 0.80
        
########################################
# actually, getting maximum of shower development for each shower,
# i.e. really Xmax, by highest bin, so no mean X, 
# but then computing the mean of these Xmax values;)
def GetHmeans(logEs, fnames, hbasename, Nshowers):
    Fs = []
    Hs = {}
    Means = {}
    Rebin = 4
        
    for logE in logEs:
        infile = None
        fname = fnames[logE]
        infile = ROOT.TFile(fname, 'read')
        Fs.append(infile)
        Hs[logE] = []
        means = []
        for i in range(0,Nshowers):
            hname = hbasename + f'_{i}'
            h = infile.Get(hname)
            try:
                mean = h.GetBinCenter(h.GetMaximumBin()) #h.GetMean()
                err = h.GetMeanError()
                means.append(mean)
                #print(mean)
                h.Rebin(Rebin)
                #if logE < 10e4:
                #    h.Rebin(2)
                Hs[logE].append(h)
            except:
                pass
                #print(f'Error getting {hname} from {fname}')

        meanMean, meanErr = GetMeanAndError(means)
        Means[logE] = showerAverResults(logE, meanMean, meanErr, means)

    return Hs, Fs, Means
        
########################################
def GetHmeansFromTree(conexDir, EconexDict, treename, varname):
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
        tree.Draw(f'{varname} >> {hname}', f'{varname} < 4000')
        # this is already a histogram ox Xmax'es!
        h = ROOT.gDirectory.Get(hname)
        #try:
        # so we should NOT take maximum of the Xmax histo, but a mean!!!
        #mean = h.GetBinCenter(h.GetMaximumBin()) #h.GetMean()
        #err = h.GetMeanError()
        # so the mean:
        mean = h.GetMean()
        err = h.GetMeanError()
        means.append(mean)
        #print(mean)
        #h.Rebin(Rebin)
        #if logE < 10e3:
        #    h.Rebin(2)
        Hs[logE].append(h)
        #meanMean, meanErr = GetMeanAndError(means)
        Means[logE] = showerAverResults(logE, mean, err, means)
        #except:
        #    print(f'Error getting conex {hname} from {fname}')


    return Hs, Fs, Means
        
        

########################################
def GetMeanAndError(means):
    meanSqSum = 0
    np = len(means)
    meanMean = sum(means) / np
    for i in range(0, len(means)):
        meanSqSum += pow(means[i] - meanMean, 2)
    meanErr = 0.
    if np > 1 and meanSqSum > 0:
        meanErr = sqrt(meanSqSum / (np - 1) / np)
        
    return meanMean, meanErr

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

    #logEs = [ int(pow(10,n)) for n in range(2,8)]
    #logEs = [ int(pow(10,n)) for n in range(3,6)]
    #logEs = [100, 1000, 10000, 50000, 100000, 1000000]
    #logEs.append(250000)

    logEs = [#11, 11.5,
        # 12, 12.5, 13, 13.5, 14, 14.5, 15,
        15.5,
        16.0,
    ]

    cnx, cny = 3, 3
    cw, ch = 1400, 1200
    print(logEs)
    
    hbasename = 'h1Nx'
    Nshowers = 2000
    fnames = {}

    if len(argv) < 3:
        print(f'Usage:   {argv[0]} rootdir model=EPOS,SIBYLL')
        print(f'Example: {argv[0]} root_Inel_0.3_C_10.0_piExp_0.2 SIBYLL')
        return()
    
    rootdir = argv[1]
    generator = argv[2] # EPOS, SIBYLL
    gBatch = False
    if len(argv) > 3 and argv[3] == '-b':
        gBatch = True
        ROOT.gROOT.SetBatch(1)

    for logE in logEs:
        fnames[logE] = f'{rootdir}/histos_p_logE_{logE:1.1f}_tmp.root'
        
    Hs, Fs, MeansAirSim = GetHmeans(logEs, fnames, hbasename, Nshowers)
    ftag = fnames[logE].split('/')[-2].replace('root_','').replace('_',' ')
    fftag = ftag.replace(' ','_')
    
    print('Got following lengths:')
    for logE in Hs:
        print(f'{logE}: {len(Hs[logE])}')
    
    gr = ROOT.TGraphErrors()
    ip = 0
    for logE,meanData in MeansAirSim.items():
        mean = meanData.mean
        meanErr = meanData.meanErr
        gr.SetPoint(ip, logE, mean)
        gr.SetPointError(ip, 0., meanErr)
        ip = ip+1


    conexDir='conex/simulated_showers/uniqueE_low/merged/' #'/home/qitek/install/conex/conex2r6.40/simulated_showers/uniqueE_low/merged'
    EconexDict = { #11: f'conex_p_E_11_{generator}_merged.root',
                   #11.5: f'conex_p_E_11.5_{generator}_merged.root',
                   #12: f'conex_p_E_12_{generator}_merged.root',
                   #12.5: f'conex_p_E_12.5_{generator}_merged.root',
                   #13: f'conex_p_E_13_{generator}_merged.root',
                   #13.5: f'conex_p_E_13.5_{generator}_merged.root',
                   #14: f'conex_p_E_14_{generator}_merged.root',
                   #14.5: f'conex_p_E_14.5_{generator}_merged.root',
                   #15: f'conex_p_E_15_{generator}_merged.root',
                   15.5: f'conex_p_E_15.5_{generator}_merged.root',
                   16: f'conex_p_E_16_{generator}_merged.root',
                   ###16.5: f'conex_p_E_16.5_{generator}_merged.root',
                  }
    cfnames = EconexDict.values()
    conexPeakXmaxHs, cFs, MeansConex = GetHmeansFromTree(conexDir, EconexDict, 'Shower', 'Xmax')
    
    gr_conex = ROOT.TGraphErrors()
    ip = 0
    ConexShowerGraphs = {}
    for logE,meanData in MeansConex.items():
        mean = meanData.mean
        meanErr = meanData.meanErr
        gr_conex.SetPoint(ip, logE, mean)
        gr_conex.SetPointError(ip, 0., meanErr)
        ip = ip+1

        # get also individual conex showers as TGraphs:
        rfile = ROOT.TFile(conexDir + EconexDict[logE], 'read')
        tree = rfile.Get('Shower')
        graphs = getConexShowerGraphs(tree, logE)
        ConexShowerGraphs[logE] = graphs

    txts = []
    

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
        
        mtxt = ROOT.TLatex(0.63, 0.68, f'Conex+{generator}')
        mtxt.SetTextColor(ROOT.kWhite)
        mtxt.SetNDC()
        mtxt.Draw()
        txts.append(mtxt)

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
    cpcan.Update()

    ########################
    # Draw conex profiles as histos:)
    canname = f'ConexHistProfiles'
    hcpcan = ROOT.TCanvas(canname, canname, 0, 0, cw, ch)
    cans.append(hcpcan)
    hcpcan.Divide(cnx, cny)
    hcpH2s = []
    ConexShowerHistos = {}
    ie = 0
    nConexDoublePeaks = {}
    ConexHsDouble = {}
    for logE,grs in ConexShowerGraphs.items():
        nConexDoublePeaks[logE] = 0
        ConexHsDouble[logE] = []
        hcpcan.cd(1+ie)
        ymax = getGrMaxima(grs)*1.2
        h2 = ROOT.TH2D(f'conexProfileHist_tmp_{logE}', ';x[g/cm^{2}];N', 100, 0, 4000, 100, 0, ymax)
        h2.Draw()
        makeWhiteAxes(h2)
        hcpH2s.append(h2)
        hs = makeHistosFromGraphs(grs, f'_{logE}')
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
            realE = pow(10, logE)
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


    cpcan.Update()
    cpcan.Print(cpcan.GetName() + f'_{generator}.pdf')
    cpcan.Print(cpcan.GetName() + f'_{generator}.png')

    
    
    
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
        ymax = getMaxima(hs)*1.2
        h2 = ROOT.TH2D(f'ctmp_{logE}', ';X_{max}[g/cm^{2}];showers', 150, 0, 1500, 100, 0, 0.25)
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
        HsDouble[logE] = []
        ymax = getMaxima(hs)*1.2
        h2 = ROOT.TH2D(f'tmp_{logE}', ';x[g/cm^{2}];Particles (e/#pi/p)', 100, 40, 4000, 100, 0, ymax)
        h2.Draw()
        makeWhiteAxes(h2)
        H2s.append(h2)

        HsPeakXmax[logE] = ROOT.TH1D(f'AirSimPeakXmax_{logE}', ';X_{max}[g/cm^{2}];showers', 75, 0, 1500)

        h2sum = ROOT.TH2D(f'hsum_{logE}', ';x[g/cm^{2}];Particles (e/#mu)', 40, 0, 4000, 25, 0, ymax)
        makeWhiteAxes(h2sum)
        Hsums.append(h2sum)

        stxt = ROOT.TLatex(0.63, 0.68, 'Private sim.')
        stxt.SetTextColor(ROOT.kWhite)
        stxt.SetNDC()
        stxt.Draw()
        txts.append(stxt)

        txt = ROOT.TLatex(0.63, 0.82, f'logE={logE}')
        txt.SetTextColor(ROOT.kWhite)
        txt.SetNDC()
        txt.Draw()
        txts.append(txt)

        ntxt = ROOT.TLatex(0.63, 0.75, f'Showers: {len(hs)}')
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
            realE = pow(10, logE)
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
        ie += 1
    ccan.Update()
    
    canname = 'GrXmean'
    gcan = ROOT.TCanvas(canname, canname, 500, 500, 800, 600)
    makeGrStyle(gr, ROOT.kAzure-3)
    gr.GetXaxis().SetTitle('log_{10}E(eV)')
    gr.GetYaxis().SetTitle('X_{max}^{N} [g/cm^{2}]')
    gr.GetYaxis().SetRangeUser(0, 1000)

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
    chi2ndf = chi2/ndf
    chtxt = '#chi^{2}/ndf = ' + f'{chi2ndf:1.1f}'
    txt = ROOT.TLatex(0.62, 0.15, chtxt)
    txt.SetNDC()
    txt.SetTextColor(ROOT.kWhite)
    txt.Draw()
    
    ROOT.gPad.Update()

    stuff.append([leg, txt])

    ########################
    # print
    pngdir  = 'png_tuning/'
    pdfdir  = 'pdf_tuning/'

    cpcan.Print(pdfdir + cpcan.GetName() + f'_{generator}.pdf')
    cpcan.Print(pngdir + cpcan.GetName() + f'_{generator}.png')
    
    hcpcan.Print(pdfdir + hcpcan.GetName() + f'_{generator}.pdf')
    hcpcan.Print(pngdir + hcpcan.GetName() + f'_{generator}.png')
    
    can.Print(pngdir + can.GetName() + f'_{fftag}.png')
    can.Print(pdfdir + can.GetName() + f'_{fftag}.pdf')

    sumcan.Print(pngdir + sumcan.GetName() + f'_{fftag}.png')
    sumcan.Print(pdfdir + sumcan.GetName() + f'_{fftag}.pdf')
    
    gcan.Print(pngdir + gcan.GetName() + f'_{generator}_{fftag}.png')
    gcan.Print(pdfdir + gcan.GetName() + f'_{generator}_{fftag}.pdf')

    ccan.Print(pngdir + ccan.GetName() + f'_{generator}_{fftag}.png')
    ccan.Print(pdfdir + ccan.GetName() + f'_{generator}_{fftag}.pdf')

    stuff.append([conexPeakXmaxHs, Hs, H2s, cH2s, Fs, cFs, gr, gr_conex])

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
