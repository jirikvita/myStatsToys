#!/usr/bin/python

import ROOT
import sys, os

#from myAll import *
stuff = []
from MakeCorrTools import *

N = 16
col = [ROOT.kRed, ROOT.kBlue, ROOT.kBlack, ROOT.kOrange, ROOT.kMagenta, ROOT.kGreen-6, ROOT.kCyan, ROOT.kPink+10]
        

#########################################
#########################################
#########################################

labels = ["Frame", "All", "Dot",  "Small blob",  "Curly track", "Heavy blob", "Heavy track",  "Straight track"]

#
# read data
#
# infilename = '/home/qitek/cernbox/TimePix/ToSort/LetNY_400x30s/txt/rate.txt'
infilename = '/home/qitek/cernbox/./TimePix/Spectra/NY_rate.txt'
pngtag='abg_extended'
frametag = '30s window'

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
        icol = 0
        for item in line.split():
            # was: Tags.append(item)
            # for head-less input file:
            Tags.append(labels[icol])
            icol = icol+1
    #else:
    if Data == {}:
        for tag in Tags:
            Data[tag] = []
    i = 0
    for item in line.split():
        Data[Tags[i]].append(float(item))
        i = i+1
    cnt = cnt+1

print(Data)
FlipData = []
N = 0
ymax = -1e6
for data in Data:
    # skip frame number and All:
    if data == labels[0] or data == labels[1]:
        continue
    FlipData.append([ data, Data[data]])
    N = max(N,len(Data[data]))+1
    ymax = max(ymax,max(Data[data]))
ymax=ymax*1.33
histo = Make2D(FlipData, len(FlipData), 'Data', frametag)
histoAll = Make2D(FlipData, len(FlipData), 'DataAll')

Cov = MakeCov(histoAll)
Corr = MakeCorr(Cov)

grs = []
for i in range(0, len(FlipData)):
    gr = MakeGraph(FlipData, i, frametag)
    grs.append(gr)



#############################
# Draw:

can = ROOT.TCanvas(pngtag, pngtag, 0, 0, 1000, 1000)
objs.append(can)
can.Divide(2,2)
can.cd(1)
#ROOT.gPad.SetGridx() ; ROOT.gPad.SetGridy()
histo.Draw("colz")

can.cd(2)
leg = ROOT.TLegend(0.45, 0.70, 0.65, 0.88)
stuff.append([can, leg])
tmp = ROOT.TH2D('tmp', 'tmp;%s;' % (frametag,), N, 0, N, 100, 0, ymax)
tmp.SetStats(0)
objs.append(tmp)
tmp.Draw()
opt = 'PL'
for gr in grs:
    gr.Draw(opt)
    opt = 'PL'
    leg.AddEntry(gr, gr.GetName().replace('_gr', ''), 'PL')
leg.Draw()

can.cd(3)
Cov.Draw('colztext')
can.cd(4)
Corr.Draw('colztext')
Corr.SetMinimum(-1.)
Corr.SetMaximum(1.)

can.Print(can.GetName() + '.png')
can.Print(can.GetName() + '.eps')


# scatter plots:

scatter = []
for i in range(0, len(FlipData)):
    for j in range(0, len(FlipData)):
        if i < j:
            sc = MakeScatterGraph(FlipData, i, j)
            scatter.append(sc)

can2 = ROOT.TCanvas(pngtag + '_scat', pngtag + '_scat', 0, 0, 1000, 1000)
nx = int(math.sqrt(len(FlipData)*len(FlipData)/2.))
can2.Divide(nx,nx)
isc = 1
for sc in scatter:
    can2.cd(isc)
    sc.Draw("AP")
    rho = sc.GetCorrelationFactor()
    tex = ROOT.TLatex(0.195, 0.83, '#rho = %1.3f' % (rho,))
    tex.SetNDC()
    tex.Draw()
    objs.append(tex)
    isc = isc+1
can2.Print(can2.GetName() + '.png')
can2.Print(can2.GetName() + '.eps')

ROOT.gApplication.Run()
