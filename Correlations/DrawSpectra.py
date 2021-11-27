#!/usr/bin/python

import ROOT
import sys, os

# Jiri Kvita June 22nd 2016, March 23rd 2017

#from myAll import *
from MakeCorrTools import *

N = 16
col = [ROOT.kRed, ROOT.kBlue, ROOT.kBlack, ROOT.kMagenta, ROOT.kGreen+2, ROOT.kOrange]


###!!!
### HOW DETAILED ANALYSIS !!!

# ???:
#Tag = ['Beta', 'Gamma', 'Alpha']
# DEFAULT:
TagDef = ['All',  'Alpha', 'Beta', 'Gama', 'Other']
# EXTENDED:
#TagExt  =[  'All',    'Dots',    'SmallBlobs',      'CurlyTracks',     'HeavyBlobs',      'HeavyTracks',     'StraightTracks']

# example:
# ./DrawSpectra.py CDGMEX_ene3.txt


#########################################
#########################################
#########################################

#
# read data
#
infilename = 'ene.txt'
pngtag='Americium_Spectra'
frametag = '10min window'
exttag = 'default'
Tag = TagDef
nx,ny = 3,1

print(sys.argv)
if len(sys.argv) > 1:
    infilenames = sys.argv[1]
    print('OK, will try to read user defined input file %s' % (infilenames,))
if len(sys.argv) > 2:
    pngtag = sys.argv[2]
    print('OK, accepting user defined tag for pictures names %s' % (pngtag,))
if len(sys.argv) > 3:
    frametag = sys.argv[3]
    print('OK, accepting user defined tag for frametag %s' % (frametag,))
if len(sys.argv) > 4:
    exttag = sys.argv[4]
    print('OK, accepting user defined tag for default/extedned! %s' % (exttag,))

if exttag.find('ext') >= 0:
    print('Switching from default analysis type to extended!')
    Tag = TagExt
    nx,ny = 3,2


    
Infilenames = []
if infilenames.find(' ') > 0:
    print('OK, we think you proveded a file list!')
    Infilenames = infilenames.split()
else:
    Infilenames.append(infilenames)

ifile = -1
Data = {}
Tags = []
for infilename in Infilenames:
    print('Reading file %s' % (infilename,))
    infile = open(infilename, 'r')
    ifile = ifile+1
    cnt = 0
    for line in infile.readlines():
        if cnt == 0:
            if ifile == 0:
                for item in line.split():
                    Tags.append(item)
        else:
            if Data == {}:
                for tag in Tags:
                    Data[tag] = []
            i = 0
            for item in line.split():
                #print '   i=%i' % (i,)
                #print '   i=%i tag: %s' % (i,Tags[i])
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

emax=15000.
histos = []
ranges=[ [100, 0, emax/40.], [30, 0, emax/1.], [100, 0, emax/5.],
         [100, 0, emax/10.], [50, 0, emax/50.], [100, 0, emax/1.], #[100, 0, emax/10.], [200, 0, emax/50.], [500, 0, emax/1.],
         [100, 0, emax], [100, 0, emax], [100, 0, emax]  ]

if exttag.find('ext') >= 0:
    ranges=[ [100, 0, emax/40.], [100, 0, emax/1.], [100, 0, emax/5.],
             [100, 0, emax/10.], [200, 0, emax/50.], [500, 0, emax/3.],
             [100, 0, emax], [100, 0, emax], [100, 0, emax]  ]


print(len(FlipData))
for i in range(0, len(FlipData)):
    histo = MakeSpectrum(FlipData, i, ranges[i])
    histos.append(histo)

#############################
# Draw:

can = ROOT.TCanvas(pngtag, pngtag, 0, 0, 1200, 500)
objs.append(can)
can.Divide(nx,ny)

j=1
logy = [1, 1, 1, 1, 1, 1, 1, 1]
for histo in histos:
    print('hname: ', histo.GetName())
    if histo.GetName().find('All') >= 0 or histo.GetName().find('Other') >= 0 or histo.GetName().find('Energy') >= 0:
        continue
    can.cd(j)
    ROOT.gPad.SetGridx()
    ROOT.gPad.SetGridy()
    ROOT.gPad.SetLogy(logy[j-1])
    histo.SetLineWidth(1)
    histo.Draw("colz")
    ROOT.gPad.Update()
    tag = '_' + histo.GetName() #Tag[j-1]
    
    ROOT.gPad.Print(can.GetName() + tag + '.png')
    #ROOT.gPad.Print(can.GetName() + tag + '.eps')
    ROOT.gPad.Print(can.GetName() + tag + '.pdf')
    #ROOT.gPad.Print(can.GetName() + tag + '.C')

    j=j+1



can.Print(can.GetName() + '.png')
can.Print(can.GetName() + '.pdf')
can.Print(can.GetName() + '.C')



ROOT.gApplication.Run()
