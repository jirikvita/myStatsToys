#!/usr/bin/python
# jk 14.12.2025

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

from mystyle import *
from myTools import *


cans = []
stuff = []

##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    #if len(sys.argv) > 1:
    #  foo = sys.argv[1]


    pngdir = 'png_Xmax/'
    pdfdir = 'pdf_Xmax/'
    os.system(f'mkdir -p {pngdir} {pdfdir}')

    ### https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    ### https://pymotw.com/2/getopt/
    ### https://docs.python.org/3.1/library/getopt.html
    gBatch = False
    gTag=''
    print(argv[1:])
   
    if gBatch:
        ROOT.gROOT.SetBatch(1)

    print('*** Settings:')
    print('tag={:}, batch={:}'.format(gTag, gBatch))

    SetDarkStyle()
    #makeDarkLegend(leg)
    #  leg = ROOT.TLegend(0.75, 0.12, 0.88, 0.45)
    #  leg.AddEntry(h], 'haha', 'L')

    #canname = 'can'
    #can2d = ROOT.TCanvas(canname, canname, 0, 0, 1000, 800)
    #cans.append(can2d)


    mode = 'ee'
    textag = mode

    #mode = 'pipi'
    #textag = '#pi#pi'
    
    gdir = 'graphs/'
    filenames = [ [f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_100.0_Gamma_10.0_mode_{mode}_xsectFrac_1.00.root', 'hist2D_StdDevVsXmax_conex_'],
                  [f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_100.0_Gamma_10.0_mode_{mode}_xsectFrac_1.00.root', 'hist2D_StdDevVsXmax_'],
                  [f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0.root', 'hist2D_StdDevVsXmax_']
                 ]

    rfiles = []
    Es = ['12.5',
          '12.75',
          '13',
          '13.25']
    
    #w = len(Es)*480
    #h = len(filenames)*480

    
    H2s = []

    # Get
    for fitems in filenames:
        fname = fitems[0]
        hbasename = fitems[1]
        rfile = ROOT.TFile(gdir + fname, 'read')
        hs2 = []
        for E in Es:
            hname = hbasename + E
            h2 = rfile.Get(hname)
            if h2 != None:
                hs2.append(h2)
            else:
                print(f'ERROR getting {hname} from {fname}')
        H2s.append(hs2)
        rfiles.append(rfile)

    # Draw
    txts = []
    H1s = []
    for i,hs2 in enumerate(H2s):
        cn = f'ShowersStdDevVsXmaxCmp{i}'
        w = 2*650
        h = 2*500
        can2d = ROOT.TCanvas(cn, cn, 0, 0, w, h)
        #can2d.Divide(len(Es), len(filenames))
        can2d.Divide(2,2)
        cans.append(can2d)
        ican = 1

        h1s = []
        for j,h2 in enumerate(hs2):
            can2d.cd(ican)
            h2.SetStats(0)
            makeWhiteAxes(h2)
            h2.Draw('colz')
            logE = Es[j]
            txt = ROOT.TLatex(0.14, 0.14, 'log_{10}' + f'E/eV={logE}, showers: {h2.GetEntries()/1000:1.1f}k')
            txt.SetTextColor(ROOT.kWhite)
            txt.SetNDC()
            txt.Draw()
            txts.append(txt)
            h1 = h2.ProjectionX()
            h1.SetName('proj_{logE}_{i}_{j}')
            h1s.append(h1)

            print(filenames[i])
            sampletag = 'Private sim.'
            if f'Zprime_100.0_Gamma_10.0_mode_{mode}' in filenames[i][0] and not 'conex' in filenames[i][1]:
                sampletag += f' incl. X#rightarrow {textag}' + ', m_{X}=100 GeV, #Gamma_{X}=10 GeV'
            if 'conex' in filenames[i][1]:
                sampletag = 'Conex'
            txt2 = ROOT.TLatex(0.14, 0.84, sampletag)
            txt2.SetTextColor(ROOT.kWhite)
            txt2.SetNDC()
            txt2.SetTextSize(0.042)
            txt2.Draw()
            txts.append(txt2)
            ican += 1
        H1s.append(h1s)

    can2d.Update()
    print(H1s)
    
    w = 650 #len(filenames)*650
    h = 600
    ican = 0
    cols = [ROOT.kMagenta-7, ROOT.kBlue-9, ROOT.kYellow, ROOT.kTeal-3] #  ROOT.kCyan-7
    legs = []
    for i,hs1 in enumerate(H1s):
        cn = f'ShowersXmaxProfileStudy{i}'
        can1d = ROOT.TCanvas(cn, cn, 0, 0, w, h)
        #can1d.Divide(len(filenames), 1)
        can1d.cd()
        cans.append(can1d)
        #ican += 1
        #can1d.cd(ican)
        
        opt = 'Chist'
        leg = ROOT.TLegend(0.55, 0.55, 0.82, 0.82)
        leg.SetTextColor(ROOT.kWhite)
        legs.append(leg)
        for j,h1 in enumerate(hs1):
            h1.SetStats(0)
            makeWhiteAxes(h1)
            h1.SetLineColor(ROOT.kAzure+10)
            h1.SetLineWidth(2)
            h1.SetLineColor(cols[j])
            h1.Scale(1./h1.Integral(0, h1.GetXaxis().GetNbins()+1))
            h1.Draw(opt)
            opt = 'Chist same'
            #ROOT.gPad.SetGridx(1)
            #ROOT.gPad.SetGridy(1)
            h1.GetXaxis().SetRangeUser(200,700)
            h1.SetMaximum(1.35 * h1.GetMaximum())
            logE = Es[j]
            leg.AddEntry(h1, 'log_{10}' + f'E/eV={logE}', 'L')
            #txt = ROOT.TLatex(0.5, 0.79, 'log_{10}' + f'E/eV={logE}')
            #txt.SetTextColor(ROOT.kWhite)
            #txt.SetNDC()
            #txt.Draw()
            #txts.append(txt)

            print(filenames[i])
            sampletag = 'Private sim.'
            if f'Zprime_100.0_Gamma_10.0_mode_{mode}' in filenames[i][0] and not 'conex' in filenames[i][1]:
                sampletag += f' incl. X#rightarrow {textag}' + ', m_{X}=100 GeV, #Gamma_{X}=10 GeV'
            if 'conex' in filenames[i][1]:
                sampletag = 'Conex'
                
            txt2 = ROOT.TLatex(0.14, 0.84, sampletag)
            txt2.SetTextColor(ROOT.kWhite)
            txt2.SetNDC()
            txt2.SetTextSize(0.035)
            txt2.Draw()
            txts.append(txt2)
        leg.Draw()
            
    
    can1d.Update()
    
    
    # Store and print
    stuff.append([H2s,rfiles])
    for can in cans:
    	can.Print(pngdir + can.GetName() + f'_{mode}.png')
    	can.Print(pdfdir + can.GetName() + f'_{mode}.pdf')
    ROOT.gPad.Update()

    ROOT.gApplication.Run()
    return

###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################

