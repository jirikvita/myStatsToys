#!/usr/bin/python

# jk 3.10.2025

import ROOT
from math import pow, log10, pow, sqrt

import os, sys

from utils import *
from consts import *

########################################

cans = []
stuff = []


###########################################################
###########################################################
###########################################################

def main(argv):

    grdir = 'graphs/'
    #generator = 'SIBYLL'
    generator = 'EPOS'
    gfilenames = {

        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0.root' : ROOT.kBlue,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_A56.root' : ROOT.kBlue + 1,
        
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_Zprime_100.0_Gamma_10.0_mode_ee_xsectFrac_0.10.root' : ROOT.kCyan,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_Zprime_100.0_Gamma_10.0_mode_ee_xsectFrac_1.00.root' : ROOT.kCyan,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_Zprime_100.0_Gamma_10.0_mode_mumu_xsectFrac_0.10.root' : ROOT.kMagenta,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_Zprime_100.0_Gamma_10.0_mode_mumu_xsectFrac_1.00.root' : ROOT.kMagenta,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_Zprime_100.0_Gamma_10.0_mode_pipi_xsectFrac_0.10.root' : ROOT.kYellow,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_Zprime_100.0_Gamma_10.0_mode_pipi_xsectFrac_1.00.root' : ROOT.kYellow,
        f'graphs_{generator}_primaryEl_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0.root' : ROOT.kWhite,
    }

    grs_conex = []
    grs = {}
    for gfilename,col in gfilenames.items():
       gfile = ROOT.TFile(grdir + gfilename, 'read')
       gfile.ls()
       grAirSim = gfile.Get('gr_airsim')
       grAirSim.SetLineColor(col)
       grAirSim.SetMarkerColor(col)
       if 'Frac_0.' in gfilename:
           grAirSim.SetLineStyle(2)
           grAirSim.SetMarkerStyle(24)

       tag = gfilename.replace(f'graphs_{generator}_', '').replace('.root', '').replace('_', ' ').replace('Gamma','#Gamma=')
       tag = tag.replace('sigmaInel','#sigma_{Inel}').replace('Csigma','#sigma_{C}').replace('xsectFrac','frac_{Z\'}').replace('mode','Z\'#rightarrow')
       tag = tag.replace('mumu','#mu#mu').replace('pipi','#pi#pi').replace('Zprime 100.0','m_{Z\'}=100 GeV').replace('10.0','10 GeV').replace('A56','Fe')
       grs[tag] = grAirSim
       funs = grAirSim.GetListOfFunctions()
       funs.Clear()
       
       if not 'Zprime' in gfilename and not 'primaryEl' in gfilename:
           gr_conex = gfile.Get('gr_conex')
           funs = gr_conex.GetListOfFunctions()
           funs.Clear()

           gr_conex.SetLineColor(ROOT.kRed)
           gr_conex.SetMarkerColor(ROOT.kRed)
           grs_conex.append(gr_conex)


    SetMyStyle()
    cw, ch = 1200, 800
    canname = f'AirSim_GrsCmp'
    can = ROOT.TCanvas(canname, canname, 0, 0, cw, ch)

    ymax = 2200
    h2 = ROOT.TH2D(f'h_tmp', ';log(E);x[g/cm^{2}];', 500, 11, 16.5, 25, 0, ymax)
    h2.SetStats(0)
    makeWhiteAxes(h2)
    stuff.append(h2)

    leg = ROOT.TLegend(0.15, 0.65, 0.85, 0.88)
    leg.SetTextColor(ROOT.kWhite)

    can.cd()
    h2.Draw()
    for gr_conex in grs_conex:
        gr_conex.Draw('PL')
        leg.AddEntry(gr_conex, f'Conex+{generator}', 'PL')

    for tag,gr in grs.items():
        gr.Draw('PL')
        leg.AddEntry(gr, tag, 'PL')

    leg.Draw()
    stuff.append([leg, can, h2, grs, grs_conex])

    pngdir = 'png_graphs/'
    pdfdir = 'pdf_graphs/'
    os.system(f'mkdir -p {pngdir} {pdfdir}')
    can.Print(pngdir + can.GetName() + f'_{generator}.png')
    can.Print(pdfdir + can.GetName() + f'_{generator}.pdf')

    ROOT.gApplication.Run()

        
        

###########################################################
###########################################################
###########################################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)

###########################################################
###########################################################
###########################################################
