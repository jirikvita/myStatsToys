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

    canname = 'can'
    can = ROOT.TCanvas(canname, canname, 0, 0, 1000, 800)
    cans.append(can)


    gdir = 'graphs/'
    filenames = [ # ['graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_100.0_Gamma_10.0_mode_ee_xsectFrac_1.00.root', 'hist2D_StdDevVsXmax_conex_'],
                  ['graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_100.0_Gamma_10.0_mode_ee_xsectFrac_1.00.root', 'hist2D_StdDevVsXmax_'],
                  ['graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0.root', 'hist2D_StdDevVsXmax_']
                  ]

    rfiles = []
    Es = ['12.5',
          '12.75',
          '13',
          '13.25']
    cn = 'ShowersStdDevVsXmaxCmp'
    w = len(Es)*480
    h = len(filenames)*480
        
    can = ROOT.TCanvas(cn, cn, 0, 0, w, h)
    can.Divide(len(Es), len(filenames))
    cans.append(can)
    Hs = []

    # Get
    for fitems in filenames:
        fname = fitems[0]
        hbasename = fitems[1]
        rfile = ROOT.TFile(gdir + fname, 'read')
        hs = []
        for E in Es:
            hname = hbasename + E
            h2 = rfile.Get(hname)
            if h2 != None:
                hs.append(h2)
            else:
                print(f'ERROR getting {hname} from {fname}')
        Hs.append(hs)
        rfiles.append(rfile)

    # Draw
    ican = 1
    txts = []
    for i,hs in enumerate(Hs):
        for j,h2 in enumerate(hs):
            can.cd(ican)
            h2.SetStats(0)
            makeWhiteAxes(h2)
            h2.Draw('colz')
            logE = E[j]
            txt = ROOT.TLatex(0.6, 0.82, f'logE={E}')
            txt.SetTextColor(ROOT.kWhite)
            txt.SetNDC()
            txt.Draw()
            txts.append(txt)

            print(filenames[i])
            if 'Zprime_100.0_Gamma_10.0_mode_ee' in filenames[i][0]:
                txt2 = ROOT.TLatex(0.14, 0.14, 'Incl. X#rightarrow ee, m_{X}=100 GeV, #Gamma_{X}=10 GeV')
                txt2.SetTextColor(ROOT.kWhite)
                txt2.SetNDC()
                txt2.SetTextSize(0.04)
                txt2.Draw()
                txts.append(txt2)
                

            ican += 1

    can.Update()
    # Store and print
    stuff.append([Hs,rfiles])
    for can in cans:
    	can.Print(can.GetName() + '.pdf')
    	can.Print(can.GetName() + '.png')
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

