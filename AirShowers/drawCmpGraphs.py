#!/usr/bin/python

# jk 3.10.2025

import ROOT
from math import pow, log10, pow, sqrt

import os, sys

from utils import *
from consts import *

from grsNames import getGrsNames

########################################

cans = []
stuff = []


###########################################################
###########################################################
###########################################################

def main(argv):

    # grdir = 'graphs_tuneBeta/'
    grdir = 'graphs/'
    #generator = 'SIBYLL'
    generator = 'EPOS'

    gfilenames = getGrsNames(generator)
    
    grs_conex = []
    grs = {}
    haveConex_p = False
    haveConex_Fe = False
    for gfilename,col in gfilenames.items():
       gfile = ROOT.TFile(grdir + gfilename, 'read')
       gfile.ls()
       grAirSim = gfile.Get('gr_airsim')
       grAirSim.SetLineColor(col)
       grAirSim.SetMarkerColor(col)
       if 'Frac_0.' in gfilename or ('EM' in gfilename and not '_p' in gfilename):
           grAirSim.SetLineStyle(2)
           grAirSim.SetMarkerStyle(24)
       if 'A56' in gfilename:
           #grAirSim.SetLineStyle(2)
           grAirSim.SetMarkerStyle(21)

       tag = gfilename.replace(f'graphs_{generator}_', '').replace('.root', '').replace('_', ' ').replace('Gamma','#Gamma=')
       tag = tag.replace('sigmaInel','#sigma_{Inel}').replace('Csigma','#sigma_{C}').replace('xsectFrac','frac_{Z\'}').replace('mode','Z\'#rightarrow')
       tag = tag.replace('mumu','#mu#mu').replace('pipi','#pi#pi').replace('Zprime 100.0','m_{Z\'}=100 GeV').replace('10.0','10 GeV').replace('A56','Fe').replace('EM','EM ').replace('length', 'X_{0}').replace('sCut',' cut').replace('1p','1.').replace('primaryE',' Electron')
       grs[tag] = grAirSim
       funs = grAirSim.GetListOfFunctions()
       funs.Clear()
       
       if (not haveConex_p or not haveConex_Fe) and not 'Zprime' in gfilename and not 'primaryE' in gfilename: # and not 'EM' in gfilename:
           gr_conex = gfile.Get('gr_conex')
           funs = gr_conex.GetListOfFunctions()
           funs.Clear()
           if 'A56' in gfilename:
               gr_conex.SetName(gr_conex.GetName() + '_Fe')
               gr_conex.SetMarkerStyle(21)
               haveConex_Fe = True
           else:
               haveConex_p = True
           gr_conex.SetLineColor(ROOT.kRed)
           gr_conex.SetMarkerColor(ROOT.kRed)
           grs_conex.append(gr_conex)


    SetMyStyle()
    cw, ch = 1200, 1200
    canname = f'AirSim_GrsCmp'
    can = ROOT.TCanvas(canname, canname, 0, 0, cw, ch)

    ymax = 2200
    x1, x2 = 11, 16.5
    h2 = ROOT.TH2D(f'h_tmp', ';log_{10}(E/eV);x[g/cm^{2}];', 500, x1, x2, 25, 0, ymax)
    h2.SetStats(0)
    makeWhiteAxes(h2)
    stuff.append(h2)

    leg = ROOT.TLegend(0.15, 0.62, 0.85, 0.89)
    leg.SetTextColor(ROOT.kWhite)

    can.cd()
    ROOT.gPad.SetGridx(1)
    ROOT.gPad.SetGridy(1)
    h2.Draw()

    # draw theory Xmax function for EM showers:
    fun_em = ROOT.TF1('Xmax_EM_theory', '[0]*(x - [1]) / log10(exp(1))', x1+0.5, x2-0.25)
    # todo: take these params from the consts.py?
    fun_em.SetParameters(37., log10(85.e6))
    stuff.append(fun_em)
    fun_em.SetLineWidth(2)
    fun_em.SetLineStyle(2)
    fun_em.SetLineColor(ROOT.kWhite)
    fun_em.Draw('same')
    
    # draw theory Xmax function for hadronic showers:
    #fun_had = ROOT.TF1('Xmax_had_theory', '[0] + [1]*(x - log(3*[2]) - 0.2*(x-15)) / log10(exp(1))', x1+0.5, x2-0.25)
    #fun_had.SetParameters(37., 120., 41.2)
    fun_had = ROOT.TF1('Xmax_had_theory', '[0] + [1]*(x-15) + 100', x1+0.5, x2-0.25)
    fun_had.SetParameters(470., 58)
    stuff.append(fun_had)
    fun_had.SetLineWidth(2)
    fun_had.SetLineStyle(2)
    fun_had.SetLineColor(ROOT.kRed-4)
    fun_had.Draw('same')
    makeWhiteAxes(fun_had)
        
    

    for gr_conex in grs_conex:
        gr_conex.Draw('PL')
        tag = ', p'
        if 'Fe' in gr_conex.GetName():
            tag = ', Fe'
        if 'Electron' in gr_conex.GetName():
            tag = ', Electron'
        leg.AddEntry(gr_conex, f'Conex+{generator}{tag}', 'PL')

    for tag,gr in grs.items():
        gr.Draw('PL')
        if ', p' in tag or 'Fe' in tag or 'Electron' in tag:
            leg.AddEntry(gr, tag, 'PL')


    leg.AddEntry(fun_em, 'Theoretical X_{max}^{EM} = X_{0} ln(E/E_{C}) [Matthews 2005]', 'L')
    leg.AddEntry(fun_had, 'Theoretical X_{max}^{had} = X_{0} + #lambda_{I} ln(E/3Nch(E)) + 100 [Matthews 2005]', 'L')
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
