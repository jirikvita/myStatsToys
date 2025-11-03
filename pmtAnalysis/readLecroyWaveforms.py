#!/usr/bin/python

# jk Oct 2025

import ROOT

import os, sys
import csv
from math import sqrt

# see $PYTHONPATH
from mystyle import *

##########################################
def main(argv):
    
    #csv_file = "lecroy/1--00001.txt"
    #csv_file = "lecroy/LED_test/C2--00001.txt"

    if len(argv) < 2:
        print(f'Usage: {argv[0]} file.csv')
        print(f'Example: {argv[0]} lecroy/LED_test/C2--00001.txt')
        return
    
    csv_file = argv[1]

    batch = False
    if len(argv) > 2:
        if argv[2] == '-b':
            batch = True
    if batch:
        ROOT.gROOT.SetBatch(1)
    tag = 'waveform_'
    try:
        tag = tag + csv_file.split('/')[-1].replace('.txt','')
    except:
        pass

    SetDarkStyle()

    grs = []
    
    # Read CSV and fill histograms
    icol = 0
    cols = [ROOT.kMagenta, ROOT.kYellow, ROOT.kCyan, ROOT.kGreen, ROOT.kRed]
    #lasttime = -1e9


    v1, v2 = -1., 0.4
    t0, t1 = 35, 140
    nb = 400
    heat2 = ROOT.TH2D('heatmap', '', nb, t0, t1, nb, v1, v2)
    

    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # skip header if exists
        for row in reader:
            time, val = 0, 0
            try:
                time = 1e9 * float(row[0])
                val = float(row[1])
                #if time - lasttime:
                #    gr = ROOT.TGraph()
                #    grs.append(gr)
                #lasttime = 1.*time
                try:
                    grs[-1].AddPoint(time, val)
                    heat2.Fill(time, val)
                except:
                    gr = ROOT.TGraph()
                    gr.SetName(f'gr_{tag}')
                    grs.append(gr)
                    grs[-1].AddPoint(time, val)

            except:
                print('Error reading line')
                print(row)


    cn = 'grcan'
    cw, ch = 800, 600
    gcan = ROOT.TCanvas(cn, cn, 0, 0, cw, ch)
    for icol,gr in enumerate(grs):
        gr.SetMarkerColor(cols[icol])
        gr.SetLineColor(cols[icol])
        gr.GetYaxis().SetTitle('A [V]')
        gr.GetXaxis().SetTitle('t [ns]')
        gr.GetYaxis().SetAxisColor(ROOT.kWhite)
        gr.GetYaxis().SetLabelColor(ROOT.kWhite)
        gr.GetYaxis().SetTitleColor(ROOT.kWhite)
        gr.Draw('AL')
        ROOT.gPad.SetGridx(1)
        ROOT.gPad.SetGridy(1)
        ROOT.gPad.Update()
        ROOT.gPad.Print(gr.GetName() + '.png')

    cn = 'heatmap'
    hcan = ROOT.TCanvas(cn, cn, 860, 0, cw, ch)
    heat2.SetStats(0)
    heat2.GetYaxis().SetAxisColor(ROOT.kWhite)
    heat2.GetYaxis().SetLabelColor(ROOT.kWhite)
    heat2.GetYaxis().SetTitleColor(ROOT.kWhite)
    heat2.GetZaxis().SetAxisColor(ROOT.kWhite)
    heat2.GetZaxis().SetLabelColor(ROOT.kWhite)
    heat2.GetZaxis().SetTitleColor(ROOT.kWhite)
    heat2.GetYaxis().SetTitle(gr.GetYaxis().GetTitle())
    heat2.GetXaxis().SetTitle(gr.GetXaxis().GetTitle())
    heat2.Draw('colz')

    if not batch:
        ROOT.gApplication.Run()



###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################
