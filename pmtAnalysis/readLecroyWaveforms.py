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
    
    csv_file = "lecroy/1--00001.txt"
    SetDarkStyle()

    grs = []
    
    # Read CSV and fill histograms
    icol = 0
    cols = [ROOT.kMagenta, ROOT.kYellow, ROOT.kCyan, ROOT.kGreen, ROOT.kRed]
    #lasttime = -1e9
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # skip header if exists
        for row in reader:
            time, val = 0, 0
            try:
                time = float(row[0])
                val = float(row[1])
                #if time - lasttime:
                #    gr = ROOT.TGraph()
                #    grs.append(gr)
                #lasttime = 1.*time
                try:
                    grs[-1].AddPoint(time, val)
                except:
                    gr = ROOT.TGraph()
                    grs.append(gr)
                    grs[-1].AddPoint(time, val)

            except:
                print('Error reading line')
                print(row)
                                
                
    for icol,gr in enumerate(grs):
        gr.SetMarkerColor(cols[icol])
        gr.SetLineColor(cols[icol])
        gr.GetYaxis().SetAxisColor(ROOT.kWhite)
        gr.GetYaxis().SetLabelColor(ROOT.kWhite)
        gr.GetYaxis().SetTitleColor(ROOT.kWhite)
        gr.Draw('AL')
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
