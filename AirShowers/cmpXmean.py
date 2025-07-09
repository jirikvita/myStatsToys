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
def GetHmeans(Es, fnames, hbasename, Nshowers):
    Fs = []
    Hs = {}
    Means = {}
    Rebin = 2
        
    for E in Es:
        infile = None
        fname = fnames[E]
        infile = ROOT.TFile(fname, 'read')
        Fs.append(infile)
        Hs[E] = []
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
                #if E < 10e3:
                #    h.Rebin(2)
                Hs[E].append(h)
            except:
                pass
                #print(f'Error getting {hname} from {fname}')

        meanMean, meanErr = GetMeanAndError(means)
        Means[E] = showerAverResults(E, meanMean, meanErr)

    return Hs, Fs, Means
        
########################################
def GetHmeansFromTree(conexDir, EconexDict, treename, varname):
    Fs = []
    Hs = {}
    Means = {}
    for E in EconexDict:
        Hs[E] = []
        means = []
        
        fname = EconexDict[E]
        rfile = ROOT.TFile(conexDir + fname, 'read')
        Fs.append(rfile)

        tree = rfile.Get(treename)
        hname = f'h_{E}'
        tree.Draw(f'{varname} >> {hname}', f'{varname} < 4000')
        h = ROOT.gDirectory.Get(hname)
        #try:
        mean = h.GetBinCenter(h.GetMaximumBin()) #h.GetMean()
        err = h.GetMeanError()
        means.append(mean)
        #print(mean)
        #h.Rebin(Rebin)
        #if E < 10e3:
        #    h.Rebin(2)
        Hs[E].append(h)
        #meanMean, meanErr = GetMeanAndError(means)
        Means[E] = showerAverResults(E, mean, err)
        #except:
        #    print(f'Error getting conex {hname} from {fname}')


    return Hs, Fs, Means
        
        

########################################
def GetMeanAndError(means):
    meanSqSum = 0
    np = len(means)
    meanMean = sum(means) / np
    for i in range(0, len(means)):
        meanSqSum = pow(means[i] - meanMean, 2)
    meanErr = 0.
    if np > 1 and meanSqSum > 0:
        meanErr = sqrt(meanSqSum / (np - 1))
        
    return meanMean, meanErr

########################################
########################################
########################################

class showerAverResults:
    def __init__(self, E, mean, meanErr):
        self.E = E
        self.mean = mean
        self.meanErr = meanErr
  
########################################
########################################
########################################
      

def main(argv):

    SetMyStyle()

    #Es = [ int(pow(10,n)) for n in range(2,8)]
    Es = [ int(pow(10,n)) for n in range(2,7)]
    #Es = [100, 1000, 10000, 50000, 100000, 1000000]
    #Es.append(250000)
    print(Es)
    
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

    for E in Es:

        fnames[E] = f'{rootdir}/histos_p_E{E}GeV_tmp.root'
        
        # HACKS:
        #fnames[E] = f'root_Inel_0.45_C_10.0_piExp_0.2_I/histos_p_E{E}GeV.root'
        #fnames[E] = f'root_Inel_0.45_C_10.0_piExp_0.2_II/histos_p_E{E}GeV.root'
        #fnames[E] = f'root_Inel_0.35_C_10.0_piExp_0.2/histos_p_E{E}GeV_tmp.root'
        #fnames[E] = f'root_Inel_0.35_C_8.0_piExp_0.15/histos_p_E{E}GeV_tmp.root'
        #fnames[E] = f'root_Inel_0.3_C_10.0_piExp_0.25/histos_p_E{E}GeV_tmp.root'
        #fnames[E] = f'root_Inel_0.3_C_10.0_piExp_0.2/histos_p_E{E}GeV_tmp.root'
        #fnames[E] = f'root_Inel_0.45_C_6.0_piExp_0.2/histos_p_E{E}GeV_tmp.root'
        #fnames[E] = f'root_Inel_0.25_C_10.0_piExp_0.2/histos_p_E{E}GeV_tmp.root'
        
        
    Hs, Fs, MeansAirSim = GetHmeans(Es, fnames, hbasename, Nshowers)
    ftag = fnames[E].split('/')[-2].replace('root_','').replace('_',' ')
    fftag = ftag.replace(' ','_')
    
    ip = 0
    print('Got following lengths:')
    for E in Hs:
        print(f'{E}: {len(Hs[E])}')
    
    gr = ROOT.TGraphErrors()
    for E,meanData in MeansAirSim.items():
        E = meanData.E
        mean = meanData.mean
        meanErr = meanData.meanErr
        gr.SetPoint(ip, log10(E) + 9, mean)
        gr.SetPointError(ip, 0., meanErr)
        ip = ip+1


    conexDir='conex/simulated_showers/uniqueE_low/merged/' #'/home/qitek/install/conex/conex2r6.40/simulated_showers/uniqueE_low/merged'
    EconexDict = { 100: f'conex_p_E_11_{generator}_merged.root',
                   1000: f'conex_p_E_12_{generator}_merged.root',
                   10000: f'conex_p_E_13_{generator}_merged.root',
                   #50000: f'conex_p_E_13.5_{generator}_merged.root',
                   100000: f'conex_p_E_14_{generator}_merged.root',
                   1000000: f'conex_p_E_15_{generator}_merged.root',
                   ###10000000: f'conex_p_E_16_{generator}_merged.root',
                  }
    cfnames = EconexDict.values()
    conexPeakXmaxHs, cFs, MeansConex = GetHmeansFromTree(conexDir, EconexDict, 'Shower', 'Xmax')
    
    gr_conex = ROOT.TGraphErrors()
    ip = 0
    ConexShowerGraphs = {}
    for E,meanData in MeansConex.items():
        E = meanData.E
        mean = meanData.mean
        meanErr = meanData.meanErr
        gr_conex.SetPoint(ip, log10(E) + 9, mean)
        gr_conex.SetPointError(ip, 0., meanErr)
        ip = ip+1

        # get also individual conex showers as TGraphs:
        rfile = ROOT.TFile(conexDir + EconexDict[E], 'read')
        tree = rfile.Get('Shower')
        graphs = getConexShowerGraphs(tree, E)
        ConexShowerGraphs[E] = graphs

    txts = []


    ########################
    # Draw conex profiles as graphs
    canname = f'ConexGrProfiles'
    cpcan = ROOT.TCanvas(canname, canname, 0, 0, 1000, 1200)
    cans.append(cpcan)
    cpcan.Divide(2,3)
    cpH2s = []
    ie = 0
    for E,grs in ConexShowerGraphs.items():
        cpcan.cd(1+ie)
        ymax = getGrMaxima(grs)*1.2
        h2 = ROOT.TH2D(f'conexProfileGr_tmp_{E}', ';x[g/cm^{2}];N', 100, 0, 4000, 100, 0, ymax)
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

        txt = ROOT.TLatex(0.63, 0.82, f'E={E/1000} TeV')
        txt.SetTextColor(ROOT.kWhite)
        txt.SetNDC()
        txt.Draw()
        txts.append(txt)
        
        ie += 1
    cpcan.Update()

    ########################
    # Draw conex profiles as histos:)
    canname = f'ConexHistProfiles'
    hcpcan = ROOT.TCanvas(canname, canname, 0, 0, 1000, 1200)
    cans.append(hcpcan)
    hcpcan.Divide(2,3)
    hcpH2s = []
    ConexShowerHistos = {}
    ie = 0
    nConexDoublePeaks = {}
    ConexHsDouble = {}
    for E,grs in ConexShowerGraphs.items():
        nConexDoublePeaks[E] = 0
        ConexHsDouble[E] = []
        hcpcan.cd(1+ie)
        ymax = getGrMaxima(grs)*1.2
        h2 = ROOT.TH2D(f'conexProfileHist_tmp_{E}', ';x[g/cm^{2}];N', 100, 0, 4000, 100, 0, ymax)
        h2.Draw()
        makeWhiteAxes(h2)
        hcpH2s.append(h2)
        hs = makeHistosFromGraphs(grs, f'_{E}')
        ConexShowerHistos[E] = hs
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
            if (E/1000 >= 100 and ( h.GetRMS() / meanMean > 0.55*( 300./E + 1. ) ) ) or (E/1000 < 100 and ( h.GetRMS() / meanMean > 0.70*( 300./E + 1. ) ) ):
                h.SetLineColor(ROOT.kRed)
                nConexDoublePeaks[E] += 1
                ConexHsDouble[E].append(h)

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

        txt = ROOT.TLatex(0.63, 0.82, f'E={E/1000} TeV')
        txt.SetTextColor(ROOT.kWhite)
        txt.SetNDC()
        txt.Draw()
        txts.append(txt)
        
        ie += 1
        
    ie = 0
    for E,hs in ConexHsDouble.items():
        hcpcan.cd(1+ie)
        for h in hs:
            h.Draw('same hist')
        ie += 1
    ie = 0
    for E,hs in ConexShowerHistos.items():
        nConexDoublePeaks[E] /= len(hs)
        print('Double peaks fraction: ', nConexDoublePeaks[E])
        hcpcan.cd(1+ie)
        txt = ROOT.TLatex(0.15, 0.82, f'Double peaks frac.: {nConexDoublePeaks[E]:1.3f}')
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
    ccan = ROOT.TCanvas(canname, canname, 0, 0, 1000, 1200)
    cans.append(ccan)
    ccan.Divide(2,3)
    cH2s = []
    ie = 0
    for E,hs in conexPeakXmaxHs.items():
        ccan.cd(1+ie)
        ymax = getMaxima(hs)*1.2
        h2 = ROOT.TH2D(f'ctmp_{E}', ';X_{max}[g/cm^{2}];showers', 150, 0, 1500, 100, 0, 0.25)
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
    can = ROOT.TCanvas(canname, canname, 0, 0, 1000, 1200)
    cans.append(can)
    can.Divide(2,3)

    canname = f'SumXmean'
    sumcan = ROOT.TCanvas(canname, canname, 600, 0, 1000, 1200)
    cans.append(sumcan)
    sumcan.Divide(2,3)


    ########################
    # Plot private shower profiles
    ie = 0
    nDoublePeaks = {}
    HsDouble = {}
    # for histograms of peak Xmax vals, to be compared to already plotted conex;-)
    HsPeakXmax = {}
    for E,hs in Hs.items():
        can.cd(1+ie)
        HsDouble[E] = []
        ymax = getMaxima(hs)*1.2
        h2 = ROOT.TH2D(f'tmp_{E}', ';x[g/cm^{2}];Particles (e/#pi/p)', 100, 40, 4000, 100, 0, ymax)
        h2.Draw()
        makeWhiteAxes(h2)
        H2s.append(h2)

        HsPeakXmax[E] = ROOT.TH1D(f'AirSimPeakXmax_{E}', ';X_{max}[g/cm^{2}];showers', 150, 0, 1500)

        h2sum = ROOT.TH2D(f'hsum_{E}', ';x[g/cm^{2}];Particles (e/#mu)', 40, 0, 4000, 25, 0, ymax)
        makeWhiteAxes(h2sum)
        Hsums.append(h2sum)

        stxt = ROOT.TLatex(0.63, 0.68, 'Private sim.')
        stxt.SetTextColor(ROOT.kWhite)
        stxt.SetNDC()
        stxt.Draw()
        txts.append(stxt)

        txt = ROOT.TLatex(0.63, 0.82, f'E={E/1000} TeV')
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
        for h in hs:
            val = h.GetMean()
            meanMean += val
            HsPeakXmax[E].Fill(val)
            #print('mean, rms: ', h.GetMean(), h.GetRMS())
        meanMean /= (1.*len(hs))
        #print('meanMean ', meanMean)
        nDoublePeaks[E] = 0.
        for h in hs:
            h.SetLineWidth(1)
            h.SetStats(0)
            #print('...drawing, mean=', h.GetMean())
            #h.Draw('hist plc' + opt)
            h.SetLineColor(ROOT.kBlue)
            if (E/1000 >= 100 and ( h.GetRMS() / meanMean > 0.55*( 300./E + 1. ) ) ) or (E/1000 < 100 and ( h.GetRMS() / meanMean > 0.70*( 300./E + 1. ) ) ):
                h.SetLineColor(ROOT.kRed)
                nDoublePeaks[E] += 1
                HsDouble[E].append(h)
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
    for E,hs in HsDouble.items():
        can.cd(1+ie)
        for h in hs:
            h.Draw('same hist')
        ie += 1
    ie = 0
    for E,hs in Hs.items():
        nDoublePeaks[E] /= len(hs)
        print('Double peaks fraction: ', nDoublePeaks[E])
        can.cd(1+ie)
        txt = ROOT.TLatex(0.15, 0.82, f'Double peaks frac.: {nDoublePeaks[E]:1.3f}')
        txt.SetNDC()
        txt.SetTextColor(ROOT.kWhite)
        txt.Draw()
        stuff.append(txt)
        ie += 1


    # plot histo of peak Xmax for AirSim into already plotted conex;-)
    ie = 0
    for E,h in HsPeakXmax.items():
        ccan.cd(1+ie)
        area = h.Integral()
        if area > 0:
            h.Scale(1./area)
        h.SetLineWidth(1)
        h.SetStats(0)
        h.SetLineColor(ROOT.kBlue)
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
    pngdir  = 'png_nPiLogEi/'
    pdfdir  = 'pdf_nPiLogEi/'

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
