#!/bin/python

import pylhe


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


def getTopPtHisto(dir):
    lhe_file = dir + "unweighted_events.lhe.gz"
    dirtag = dir.replace('/','')
    hn = 'h_pt_t_' + dirtag
    h_pt_t = ROOT.TH1D(hn, ';p_{T}^{t} [GeV];unw. events', 100, 0, 500)
    hn = 'h_y_t_' + dirtag
    h_y_t = ROOT.TH1D(hn, ';y^{t};unw. events', 100, -5, 5)
    print(f'Analyzing file {lhe_file}')
    #for i, event in enumerate(pylhe.read_lhe(lhe_file)):
    for i,event in enumerate(pylhe.LHEFile.fromfile(lhe_file).events):
        #print(f"Event {i}, weights = {event.weights}")
        if i % 1000 == 0:
            print(f"Processing event {i}")
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

        #if i > 1010:
        #    break
    return [h_pt_t, h_y_t]
            

dirs = [ 'nNNPDF10_nlo_as_0118_Pb208/',
         'NNPDF23_nlo_as_0118/'
        ]

hsall = {}
for dir in dirs:
    dirtag = dir.replace('/','')
    hsall[dirtag] = getTopPtHisto(dir)

same = ''
cols = [ROOT.kRed, ROOT.kBlue]
legs = []
cn = 'cmpLhePdfs'
can = ROOT.TCanvas(cn, cn)
can.Divide(2,2)
for ih,tag in enumerate(hsall):
    legs.append(ROOT.TLegend(0.45, 0.65, 0.88, 0.88))
    hs = hsall[tag]
    for ic,h in enumerate(hs):
        can.cd(ic+1)
        h.SetStats(0)
        h.SetLineColor(cols[ih])
        h.Draw('hist' + same)
        legs[-1].AddEntry(h, tag, 'PL')
    same = 'same'
for ic,hs in enumerate(hsall):
    can.cd(ic+1)
    legs[ic].Draw()

ROOT.gPad.Update()
ROOT.gApplication.Run()
