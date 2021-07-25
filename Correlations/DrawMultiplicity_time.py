#!/usr/bin/python

import ROOT
import sys, os

# Jiri Kvita June 22nd 2016, March 23rd 2017

from myAll import *
from MakeCorrTools import *

N = 16
col = [ROOT.kRed, ROOT.kBlue, ROOT.kBlack]
        

#########################################
#########################################
#########################################

#
# read data
#
infilename = 'all_jeskyneII.txt'
pngtag='Multiplicity_time'
frametag = '10min window'

print sys.argv
if len(sys.argv) > 1:
    infilename = sys.argv[1]
    print 'OK, will try to read user defined file %s' % (infilename,)
if len(sys.argv) > 2:
    pngtag = sys.argv[2]
    print 'OK, accepting user defined tag for pictures names %s' % (pngtag,)
if len(sys.argv) > 3:
    frametag = sys.argv[3]
    print 'OK, accepting user defined tag for pictures names %s' % (frametag,)




infile = open(infilename, 'read')
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

# frames:
emax=770
bins=770

histos = []
ranges=[ [bins, 0, emax], [bins, 0, emax], [bins, 0, emax], [bins, 0, emax], [200, 0, emax], [bins, 0, emax], [bins, 0, emax], [bins, 0, emax]]
print len(FlipData)
for i in range(0, len(FlipData)):
    histo = MakeSpectrum(FlipData, i, ranges[i])
    histos.append(histo)
    histo.GetXaxis().SetTitle('frame of 5min')
    
#############################
# Draw:

can = nextCan.nextTCanvas(pngtag, pngtag, 0, 0, 1000, 1000)
objs.append(can)
#can.Divide(3,1)

j=1
logy = [0, 0, 0]

for histo in histos:
    if histo.GetName().find('Other') >= 0 or histo.GetName().find('Energy') >= 0 or histo.GetName().find('Frame') >= 0:
        continue
    can.cd(j)
    ROOT.gPad.SetGridx()
    ROOT.gPad.SetGridy()
    ROOT.gPad.SetLogy(logy[j-1])
    histo.Scale(1.)
    histo.SetStats(0)
    histo.Draw("colz")
    j=j+1

# t0: 16h14miin
t0=(16*60+14)/5 # 5min blocks
day=(24*60)/5 # 5min blocks
Midnights=[day-t0, 2*day-t0, 3*day-t0]
Days = ['Saturday!', 'Sunday!', 'Monday...']
lines = []
for day,mid in zip(Days,Midnights):
    line = ROOT.TLine(mid, histos[0].GetMinimum(), mid, histos[0].GetMaximum())
    line.SetLineColor(ROOT.kRed)
    line.SetLineWidth(2)
    line.Draw()
    lines.append(line)
    txt = ROOT.TLatex(mid+0.4,  histos[0].GetMaximum(),day)
    txt.SetTextSize(0.03)
    #txt.SetNDC()
    txt.SetTextColor(ROOT.kRed)
    txt.Draw()
    lines.append(txt)

can.Print(can.GetName() + '.png')
can.Print(can.GetName() + '.eps')
can.Print(can.GetName() + '.pdf')
can.Print(can.GetName() + '.C')



ROOT.gApplication.Run()
