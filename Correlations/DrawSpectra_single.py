#!/usr/bin/python

import ROOT
import sys, os

# Jiri Kvita June 22nd 2016, March 23rd 2017

#from myAll import *
from MakeCorrTools import *

N = 16
col = [ROOT.kRed, ROOT.kBlue, ROOT.kBlack]
        

#########################################
#########################################
#########################################

#
# read data
#
infilename = 'ene_jeskyneII.txt'
pngtag='All_Spectra'
frametag = '10min window'

print(sys.argv)
if len(sys.argv) > 1:
    infilename = sys.argv[1]
    print('OK, will try to read user defined file %s' % (infilename,))
if len(sys.argv) > 2:
    pngtag = sys.argv[2]
    print('OK, accepting user defined tag for pictures names %s' % (pngtag,))
if len(sys.argv) > 3:
    frametag = sys.argv[3]
    print('OK, accepting user defined tag for pictures names %s' % (frametag,))




infile = open(infilename, 'r')
Tags = []
cnt = 0
Data = {}
for line in infile.readlines():
    if cnt == 0:
        for item in line.split():
            Tags.append(item)
    else:
        if Data == {}:
            for tag in Tags:
                Data[tag] = []
        i = 0
        for item in line.split():
            Data[Tags[i]].append(float(item))
            i = i+1
    cnt = cnt+1

#print Data
FlipData = []
N = 0
ymax = -1e6
for data in Data:
    FlipData.append([ data, Data[data]])
    N = max(N,len(Data[data]))+1
    
#print FlipData

# energy:
emax=13000.
bins=100

histos = []
ranges=[ [bins, 0, emax], [bins, 0, emax], [bins, 0, emax], [bins, 0, emax], [200, 0, emax], [bins, 0, emax], [bins, 0, emax], [bins, 0, emax]]
print(len(FlipData))
for i in range(0, len(FlipData)):
    histo = MakeSpectrum(FlipData, i, ranges[i])
    histos.append(histo)
    histo.GetXaxis().SetTitle('E [keV]')
    histo.GetYaxis().SetTitleOffset(2.2)
    
#############################
# Draw:

ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gStyle.SetPadRightMargin(0.05)


can = ROOT.TCanvas(pngtag, pngtag, 0, 0, 850, 800)
objs.append(can)
#can.Divide(3,1)

j=1
logy = [0, 0, 0]

for histo in histos:
    if histo.GetName().find('Other') >= 0 or histo.GetName().find('Energy') >= 0 or histo.GetName().find('Frame') >= 0:
        continue
    can.cd(j)
    #ROOT.gPad.SetGridx()
    #ROOT.gPad.SetGridy()
    ROOT.gPad.SetLogy(logy[j-1])
    histo.Scale(1.)
    histo.SetStats(0)
    histo.Draw("colz")
    j=j+1



can.Print(can.GetName() + '.png')
can.Print(can.GetName() + '.pdf')
can.Print(can.GetName() + '.C')



ROOT.gApplication.Run()
