#!/bin/python

# jk 16.1.2026

import pylhe

import os, sys
import ROOT

from math import *

"""
p.id        # PDG ID
p.status    # status code
p.px, p.py, p.pz, p.e
p.m
p.mother1, p.mother2
p.color1, p.color2
"""

# todo: check the status of particles!

#########################################################################
def getTopPtHisto(dir):
    lhe_file = dir + "unweighted_events.lhe.gz"
    dirtag = dir.replace('/','')
    
    hn = 'h_pt_t_' + dirtag
    h_pt_t = ROOT.TH1D(hn, ';p_{T}^{t} [GeV];unw. events', 100, 0, 500)

    hn = 'h_y_t_' + dirtag
    h_y_t = ROOT.TH1D(hn, ';y^{t};unw. events / N', 100, -5, 5)

    hn = 'h_y_tt_' + dirtag
    h_y_tt = ROOT.TH1D(hn, ';y^{tt};unw. events / N', 100, -5, 5)
    
    hn = 'h_pt_tt_' + dirtag
    h_pt_tt = ROOT.TH1D(hn, ';p_{T}^{tt};unw. events / N', 100, 0, 300)
    
    hn = 'h_m_tt_' + dirtag
    h_m_tt = ROOT.TH1D(hn, ';m^{tt};unw. events / N', 400, 0, 1000)
    
    print(f'Analyzing file {lhe_file}')
    #for i, event in enumerate(pylhe.read_lhe(lhe_file)):
    for i,event in enumerate(pylhe.LHEFile.fromfile(lhe_file).events):
        #print(f"Event {i}, weights = {event.weights}")
        if i % 1000 == 0:
            print(f"Processing event {i}")
        t = ROOT.TLorentzVector()
        tbar = ROOT.TLorentzVector()
        for p in event.particles:
            #print(f" id={p.id:6d} status={p.status:2d} px={p.px:8.3f} py={p.py:8.3f} pz={p.pz:8.3f} E={p.e:8.3f}")
            if abs(p.id) == 6:
                pt = sqrt( pow(p.px,2) + pow(p.py,2) )
                h_pt_t.Fill(pt)
                try:
                    y = 0.5*log( (p.e + p.pz) / (p.e - p.pz) )
                    h_y_t.Fill(y)
                except:
                    pass
                if p.id < 0:
                    tbar.SetPxPyPzE(p.px, p.py, p.pz, p.e)
                else:
                    t.SetPxPyPzE(p.px, p.py, p.pz, p.e)
        if t.E() > 0 and tbar.E() > 0:
            # mtt, ytt
            ttbar = t + tbar
            h_pt_tt.Fill(ttbar.Pt())
            h_m_tt.Fill(ttbar.M())
            h_y_tt.Fill(ttbar.Rapidity())
        # hacks
        #if i > 10:
        #    break
    return [h_pt_t, h_y_t, h_y_tt, h_m_tt, h_pt_tt]

#########################################################################
def main(argv):
    
    dirs = [ 'nNNPDF10_nlo_as_0118_Pb208/',
             'NNPDF23_nlo_as_0118/'
            ]

    # Analyze and get histos:
    hsall = {}
    for dir in dirs:
        dirtag = dir.replace('/','')
        hsall[dirtag] = getTopPtHisto(dir)

    # Plot
    same = ''
    cols = [ROOT.kRed, ROOT.kBlue, ROOT.kBlack, ROOT.kGreen+2, ROOT.kCyan, ROOT.kMagenta]
    legs = []
    cn = 'cmpLhePdfs'
    can = ROOT.TCanvas(cn, cn)
    can.Divide(3,2)

    for ipdf,tag in enumerate(hsall):
        hs = hsall[tag]
        for ic,h in enumerate(hs):
            if ipdf == 0:
                legs.append(ROOT.TLegend(0.45, 0.65, 0.88, 0.88))
            can.cd(ic+1)
            ROOT.gPad.SetLogy(1)
            h.SetStats(0)
            h.Scale(1./h.Integral())
            h.SetLineColor(cols[ipdf])
            h.Draw('hist' + same)
            legs[ic].AddEntry(h, tag + f' Mean,StdDev: {h.GetMean():1.3f},{h.GetStdDev():1.3f}', 'PL')
        same = 'same'

    for ic,hs in enumerate(hsall[tag]):
        can.cd(ic+1)
        legs[ic].Draw()

    ROOT.gPad.Update()
    can.Print(can.GetName() + '.png')
    can.Print(can.GetName() + '.pdf')
    ROOT.gApplication.Run()


#########################################################################
#########################################################################
#########################################################################

if __name__ == '__main__':
    main(sys.argv)


#########################################################################
#########################################################################
#########################################################################
